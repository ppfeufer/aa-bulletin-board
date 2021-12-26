"""
Testing access to bulletins
"""

# Third Party
from faker import Faker

# Django
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from ..models import Bulletin
from .utils import create_fake_user

fake = Faker()


class TestBulletin(TestCase):
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

    def test_should_show_dashboard(self):
        """
        Test that a user with basic_access can see the bulletin board
        :return:
        :rtype:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("aa_bulletin_board:dashboard"))

        # then
        self.assertEqual(res.status_code, 200)

    def test_should_show_bulletin(self):
        """
        Test that a user with basic_access can see the bulletin
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(
            reverse("aa_bulletin_board:view_bulletin", kwargs={"slug": bulletin.slug})
        )
        result = Bulletin.objects.user_has_access(self.user_1002)

        # then
        self.assertEqual(res.status_code, 200)
        self.assertIn(bulletin, result)

    def test_should_not_show_dashboard(self):
        """
        Test that a user without basic_access can't see the bulletin board
        :return:
        :rtype:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("aa_bulletin_board:dashboard"))

        # then
        self.assertIsNot(res.status_code, 200)

    def test_should_not_show_bulletin(self):
        """
        Test that a user without basic_access can't see the bulletin
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(
            reverse("aa_bulletin_board:view_bulletin", kwargs={"slug": bulletin.slug})
        )

        # then
        self.assertIsNot(res.status_code, 200)

    def test_should_return_bulletin_for_user_with_perm_manage_bulletins(self):
        """
        Test that a user with "aa_bulletin_board.manage_bulletins" can see all bulletins
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        # when
        result = Bulletin.objects.user_has_access(self.user_1003)

        # then
        self.assertIn(bulletin, result)

    def test_should_return_restricted_bulletin_for_user_with_perm_manage_bulletins(
        self,
    ):
        """
        Test that a user with "aa_bulletin_board.manage_bulletins"
        can see all bulletins, even restricted
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )
        bulletin.groups.add(self.group)

        # when
        result = Bulletin.objects.user_has_access(self.user_1003)

        # then
        self.assertIn(bulletin, result)

    def test_should_return_bulletin_with_no_groups(self):
        """
        Test that any user with access can se non restricted bulletins
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        # when
        result = Bulletin.objects.user_has_access(self.user_1002)

        # then
        self.assertIn(bulletin, result)

    def test_should_return_bulletin_for_group_member(self):
        """
        Test that group restricted bulletins are visible for users who have this group
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )
        bulletin.groups.add(self.group)
        self.user_1001.groups.add(self.group)

        # when
        result = Bulletin.objects.user_has_access(self.user_1001)

        # then
        self.assertIn(bulletin, result)

    def test_should_not_return_bulletin_for_non_group_member(self):
        """
        Test that group restricted bulletins are not visible for
        users who don't have this group
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1002,
        )
        bulletin.groups.add(self.group)

        # when
        result = Bulletin.objects.user_has_access(self.user_1002)

        # then
        self.assertNotIn(bulletin, result)
