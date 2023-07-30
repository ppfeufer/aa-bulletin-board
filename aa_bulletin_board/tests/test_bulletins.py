"""
Test bulletins
"""

# Third Party
from faker import Faker

# Django
from django.contrib.auth.models import Group, User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

# AA Bulletin Board
from aa_bulletin_board.forms import BulletinForm
from aa_bulletin_board.helpers import string_cleanup
from aa_bulletin_board.models import Bulletin, get_sentinel_user
from aa_bulletin_board.tests.utils import create_fake_user

fake = Faker()


class TestGetSentinelUser(TestCase):
    """
    Tests for the sentinel user
    """

    def test_should_create_user_when_it_does_not_exist(self):
        """
        Test should create a sentinel user when it doesn't exist
        :return:
        """

        # when
        user = get_sentinel_user()

        # then
        self.assertEqual(user.username, "deleted")

    def test_should_return_user_when_it_does(self):
        """
        Test should return sentinel user when it exists
        :return:
        """

        # given
        User.objects.create_user(username="deleted")

        # when
        user = get_sentinel_user()

        # then
        self.assertEqual(user.username, "deleted")


class TestBulletins(TestCase):
    """
    Test Bulletins
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()
        cls.group = Group.objects.create(name="Superhero")

        # User cannot access bulletins
        cls.user_1001 = create_fake_user(1001, "Peter Parker")

        # User can access bulletins
        cls.user_1002 = create_fake_user(
            1002, "Bruce Wayne", permissions=["aa_bulletin_board.basic_access"]
        )

        # User can manage bulletins
        cls.user_1003 = create_fake_user(
            1003,
            "Clark Kent",
            permissions=[
                "aa_bulletin_board.basic_access",
                "aa_bulletin_board.manage_bulletins",
            ],
        )

    def test_should_remove_bulletin(self):
        """
        Test if a bulletin should be removed
        :return:
        :rtype:
        """

        # given
        bulletin_title = fake.sentence()
        bulletin = Bulletin.objects.create(
            title=bulletin_title,
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(
            reverse("aa_bulletin_board:remove_bulletin", args=[bulletin.slug])
        )
        messages = list(get_messages(response.wsgi_request))

        # then
        self.assertRedirects(response, "/bulletin-board/")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Bulletin "{bulletin_title}" deleted.')

    def test_should_raise_does_not_exist_exception_when_delete_bulletin_not_found(self):
        """
        Test if a bulletin that doesn't exist should be removed
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title=fake.sentence(),
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(
            reverse("aa_bulletin_board:remove_bulletin", args=["foobarsson"])
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertRaises(bulletin.DoesNotExist)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "The bulletin you are trying to delete does not exist.",
        )

    def test_should_raise_does_not_exist_exception_when_edit_bulletin_not_found(self):
        """
        Test if a bulletin that doesn't exist should be edited
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title=fake.sentence(),
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(
            reverse("aa_bulletin_board:edit_bulletin", args=["foobarsson"])
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertRaises(bulletin.DoesNotExist)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "The bulletin you are trying to edit does not exist.",
        )

    def test_should_translate_russian_letters_in_slug(self):
        """
        Test that russian letters in a slug are translated
        :return:
        :rtype:
        """

        bulletin = Bulletin.objects.create(
            title="дрифтерке, рорки в док",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        self.assertEqual(bulletin.slug, "drifterke-rorki-v-dok")

    def test_should_return_cleaned_message_string_on_bulletin_creation(self):
        """
        Test should return a clean/sanitized message string when a new bulletin is created
        :return:
        """

        # given
        dirty_message = (
            'this is a script test. <script type="text/javascript">alert('
            "'test')</script>and this is style test. <style>.MathJax, "
            ".MathJax_Message, .MathJax_Preview{display: none}</style>end tests."
        )
        cleaned_message = string_cleanup(dirty_message)
        bulletin = Bulletin.objects.create(
            title="Foobar",
            content=dirty_message,
            created_by=self.user_1001,
        )

        self.assertEqual(bulletin.content, cleaned_message)

    def test_bulletin_slug_creation(self):
        """
        Test slug creation
        :return:
        :rtype:
        """

        bulletin = Bulletin.objects.create(
            title="This is a bulletin",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        bulletin_2 = Bulletin.objects.create(
            title="This is a bulletin",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        bulletin_3 = Bulletin.objects.create(
            title="This is a bulletin",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        self.assertEqual(bulletin.slug, "this-is-a-bulletin")
        self.assertEqual(bulletin_2.slug, "this-is-a-bulletin-1")
        self.assertEqual(bulletin_3.slug, "this-is-a-bulletin-2")

    def test_should_return_bulletin_title_as_model_object_string_name(self):
        """
        Test should return the object's string name
        :return:
        :rtype:
        """

        bulletin = Bulletin.objects.create(
            title="This is a bulletin",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        self.assertEqual(str(bulletin), "This is a bulletin")

    def test_form_clean_content_method(self):
        """
        Test the clean_ method of the form
        :return:
        :rtype:
        """

        dirty_message = (
            'this is a script test. <script type="text/javascript">alert('
            "'test')</script>and this is style test. <style>.MathJax, "
            ".MathJax_Message, .MathJax_Preview{display: none}</style>end tests."
        )
        cleaned_message = string_cleanup(dirty_message)
        data = {"title": "This is a title", "content": dirty_message}

        form = BulletinForm(data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["content"], cleaned_message)
