"""
Test for the UI
"""

# Third Party
from django_webtest import WebTest
from faker import Faker

# Django
from django.contrib.auth.models import Group
from django.urls import reverse

from ..models import Bulletin
from .utils import create_fake_user

fake = Faker()


class TestBulletinUI(WebTest):
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
