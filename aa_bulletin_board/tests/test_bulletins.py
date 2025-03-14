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
from aa_bulletin_board.helper.string import string_cleanup
from aa_bulletin_board.models import Bulletin, get_sentinel_user
from aa_bulletin_board.tests.utils import create_fake_user

fake = Faker()


class TestGetSentinelUser(TestCase):
    """
    Tests for the sentinel user
    """

    def test_should_create_user_when_it_does_not_exist(self) -> None:
        """
        Test should create a sentinel user when it doesn't exist

        :return:
        :rtype:
        """

        # when
        user = get_sentinel_user()

        # then
        self.assertEqual(first=user.username, second="deleted")

    def test_should_return_user_when_it_does(self) -> None:
        """
        Test should return sentinel user when it exists

        :return:
        :rtype:
        """

        # given
        User.objects.create_user(username="deleted")

        # when
        user = get_sentinel_user()

        # then
        self.assertEqual(first=user.username, second="deleted")


class TestBulletins(TestCase):
    """
    Test Bulletins
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users

        :return:
        :rtype:
        """

        super().setUpClass()
        cls.group = Group.objects.create(name="Superhero")

        # User cannot access bulletins
        cls.user_1001 = create_fake_user(
            character_id=1001, character_name="Peter Parker"
        )

        # User can access bulletins
        cls.user_1002 = create_fake_user(
            character_id=1002,
            character_name="Bruce Wayne",
            permissions=["aa_bulletin_board.basic_access"],
        )

        # User can manage bulletins
        cls.user_1003 = create_fake_user(
            character_id=1003,
            character_name="Clark Kent",
            permissions=[
                "aa_bulletin_board.basic_access",
                "aa_bulletin_board.manage_bulletins",
            ],
        )

    def test_should_remove_bulletin(self) -> None:
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

        self.client.force_login(user=self.user_1003)

        # when
        response = self.client.get(
            path=reverse(
                viewname="aa_bulletin_board:remove_bulletin", args=[bulletin.slug]
            )
        )
        messages = list(get_messages(request=response.wsgi_request))

        # then
        self.assertRedirects(response=response, expected_url="/bulletin-board/")
        self.assertEqual(first=len(messages), second=1)
        self.assertEqual(
            first=str(messages[0]), second=f'Bulletin "{bulletin_title}" deleted.'
        )

    def test_should_raise_does_not_exist_exception_when_delete_bulletin_not_found(
        self,
    ) -> None:
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
        self.client.force_login(user=self.user_1003)

        # when
        response = self.client.get(
            path=reverse(
                viewname="aa_bulletin_board:remove_bulletin", args=["foobarsson"]
            )
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertRaises(expected_exception=bulletin.DoesNotExist)
        self.assertEqual(first=len(messages), second=1)
        self.assertEqual(
            first=str(messages[0]),
            second="The bulletin you are trying to delete does not exist.",
        )

    def test_should_raise_does_not_exist_exception_when_edit_bulletin_not_found(
        self,
    ) -> None:
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
        self.client.force_login(user=self.user_1003)

        # when
        response = self.client.get(
            path=reverse(
                viewname="aa_bulletin_board:edit_bulletin", args=["foobarsson"]
            )
        )
        messages = list(get_messages(request=response.wsgi_request))

        self.assertRaises(expected_exception=bulletin.DoesNotExist)
        self.assertEqual(first=len(messages), second=1)
        self.assertEqual(
            first=str(messages[0]),
            second="The bulletin you are trying to edit does not exist.",
        )

    def test_should_translate_russian_letters_in_slug(self) -> None:
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

        self.assertEqual(first=bulletin.slug, second="drifterke-rorki-v-dok")

    def test_should_return_cleaned_message_string_on_bulletin_creation(self) -> None:
        """
        Test should return a clean/sanitized message string
        when a new bulletin is created

        :return:
        :rtype:
        """

        # given
        dirty_message = (
            'this is a script test. <script type="text/javascript">alert('
            "'test')</script>and this is style test. <style>.MathJax, "
            ".MathJax_Message, .MathJax_Preview{display: none}</style>end tests."
        )
        cleaned_message = string_cleanup(string=dirty_message)
        bulletin = Bulletin.objects.create(
            title="Foobar",
            content=dirty_message,
            created_by=self.user_1001,
        )

        self.assertEqual(first=bulletin.content, second=cleaned_message)

    def test_bulletin_slug_creation(self) -> None:
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

        self.assertEqual(first=bulletin.slug, second="this-is-a-bulletin")
        self.assertEqual(first=bulletin_2.slug, second="this-is-a-bulletin-1")
        self.assertEqual(first=bulletin_3.slug, second="this-is-a-bulletin-2")

    def test_should_return_bulletin_title_as_model_object_string_name(self) -> None:
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

        self.assertEqual(first=str(bulletin), second="This is a bulletin")

    def test_form_clean_content_method(self) -> None:
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
        cleaned_message = string_cleanup(string=dirty_message)
        data = {"title": "This is a title", "content": dirty_message}

        form = BulletinForm(data=data)

        self.assertTrue(expr=form.is_valid())
        self.assertEqual(first=form.cleaned_data["content"], second=cleaned_message)
