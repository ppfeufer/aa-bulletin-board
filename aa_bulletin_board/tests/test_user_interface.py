"""
Test for the UI
"""

# Third Party
from django_webtest import WebTest
from faker import Faker

# Django
from django.contrib.auth.models import Group
from django.urls import reverse

# AA Bulletin Board
from aa_bulletin_board.helpers import string_cleanup
from aa_bulletin_board.models import Bulletin
from aa_bulletin_board.tests.utils import create_fake_user

fake = Faker()


class TestBulletinUI(WebTest):
    """
    Test Bulletin UI
    """

    @classmethod
    def setUpClass(cls):
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

    def test_should_show_bulletin_page(self):
        """
        Test if a bulletin is shown
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Test Bulletin",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1002,
        )
        self.app.set_user(self.user_1002)

        # when
        page = self.app.get(
            reverse("aa_bulletin_board:view_bulletin", args=[bulletin.slug])
        )

        # then
        self.assertTemplateUsed(page, "aa_bulletin_board/bulletin.html")

    def test_should_redirect_to_bulletin_dashboard_when_bulletin_does_not_exist(self):
        """
        Test should redirect to bulletin dashboard when bulletin does not exist
        :return:
        :rtype:
        """

        # given
        self.app.set_user(self.user_1002)

        # when
        page = self.app.get(reverse("aa_bulletin_board:view_bulletin", args=["foobar"]))

        # then
        self.assertRedirects(page, "/bulletin-board/")

    def test_should_show_create_bulletin_page(self):
        """
        Test if create bulletin is shown
        :return:
        :rtype:
        """

        # given
        self.app.set_user(self.user_1003)

        # when
        page = self.app.get(reverse("aa_bulletin_board:create_bulletin"))

        # then
        self.assertTemplateUsed(page, "aa_bulletin_board/edit-bulletin.html")

    def test_should_show_edit_bulletin_page(self):
        """
        Test if edit bulletin is shown
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Test Bulletin",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1002,
        )
        self.app.set_user(self.user_1003)

        # when
        page = self.app.get(
            reverse("aa_bulletin_board:edit_bulletin", args=[bulletin.slug])
        )

        # then
        self.assertTemplateUsed(page, "aa_bulletin_board/edit-bulletin.html")

    def test_should_redirect_to_bulletin_dashboard_when_edit_bulletin_does_not_exist(
        self,
    ):
        """
        Test should redirect to bulletin dashboard when bulletin to edit does not exist
        :return:
        :rtype:
        """

        # given
        self.app.set_user(self.user_1003)

        # when
        page = self.app.get(reverse("aa_bulletin_board:edit_bulletin", args=["foobar"]))

        # then
        self.assertRedirects(page, "/bulletin-board/")

    def test_should_return_cleaned_message_string_on_bulletin_creation(self):
        """
        Test should return a clean/sanitized message string when a new bulletin is created
        :return:
        """

        # given
        self.app.set_user(self.user_1003)
        page = self.app.get(reverse("aa_bulletin_board:create_bulletin"))
        dirty_message = (
            'this is a script test. <script type="text/javascript">alert('
            "'test')</script>and this is style test. <style>.MathJax, "
            ".MathJax_Message, .MathJax_Preview{display: none}</style>end tests."
        )
        cleaned_message = string_cleanup(dirty_message)

        # when
        form = page.forms["aa-bulletin-board-bulletin-form"]
        form["title"] = "Message Cleanup Test"
        form["content"] = dirty_message
        form.submit().follow()

        # then
        new_bulletin = Bulletin.objects.last()
        self.assertEqual(new_bulletin.content, cleaned_message)

    def test_should_return_cleaned_message_string_on_bulletin_edit(self):
        """
        Test should return a clean/sanitized message string when a bulletin is edited
        :return:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Test Bulletin 2",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1002,
        )
        self.app.set_user(self.user_1003)

        # when
        page = self.app.get(
            reverse("aa_bulletin_board:edit_bulletin", args=[bulletin.slug])
        )
        dirty_message = (
            'this is a script test. <script type="text/javascript">alert('
            "'test')</script>and this is style test. <style>.MathJax, "
            ".MathJax_Message, .MathJax_Preview{display: none}</style>end tests."
        )
        cleaned_message = string_cleanup(dirty_message)

        form = page.forms["aa-bulletin-board-bulletin-form"]
        form["title"] = "Message Cleanup Test"
        form["content"] = dirty_message
        form.submit().follow()

        # then
        bulletin_edited = Bulletin.objects.get(pk=bulletin.pk)
        self.assertEqual(bulletin_edited.content, cleaned_message)

    def test_should_return_to_edit_bulletin_form_for_invalid_form_submitted_on_create_bulletin(
        self,
    ):
        """
        Test should return to the bulletin form, because the submitted form is not valid
        due to missing title
        :return:
        :rtype:
        """

        self.app.set_user(self.user_1003)
        page = self.app.get(reverse("aa_bulletin_board:create_bulletin"))

        # when
        form = page.forms["aa-bulletin-board-bulletin-form"]
        form["content"] = "Lorem Ipsum"
        page = form.submit()

        # then
        self.assertTemplateUsed(page, "aa_bulletin_board/edit-bulletin.html")

    def test_should_return_to_edit_bulletin_form_for_invalid_form_submitted_on_edit_bulletin(
        self,
    ):
        """
        Test should return to the bulletin form, because the submitted form is not valid
        due to missing title
        :return:
        :rtype:
        """

        bulletin = Bulletin.objects.create(
            title="Test Bulletin",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1002,
        )
        self.app.set_user(self.user_1003)

        # when
        page = self.app.get(
            reverse("aa_bulletin_board:edit_bulletin", args=[bulletin.slug])
        )

        # when
        form = page.forms["aa-bulletin-board-bulletin-form"]
        form["title"] = ""
        form["content"] = "Lorem Ipsum"
        page = form.submit()

        # then
        self.assertTemplateUsed(page, "aa_bulletin_board/edit-bulletin.html")
