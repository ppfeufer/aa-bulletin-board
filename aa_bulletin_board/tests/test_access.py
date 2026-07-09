"""
Testing access to bulletins
"""

# Standard Library
from http import HTTPStatus

# Third Party
from faker import Faker

# Django
from django.urls import reverse

# Alliance Auth
from allianceauth.groupmanagement.models import Group

# AA Bulletin Board
from aa_bulletin_board.models import Bulletin
from aa_bulletin_board.tests import BaseTestCase
from aa_bulletin_board.tests.utils import create_fake_user, random_id

fake = Faker()


class TestAccess(BaseTestCase):
    """
    Test access to the module
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
        cls.user_without_access = create_fake_user(
            character_id=random_id(), character_name="Peter Parker"
        )

        # User can access bulletins
        cls.user_with_basic_access = create_fake_user(
            character_id=random_id(),
            character_name="Bruce Wayne",
            permissions=["aa_bulletin_board.basic_access"],
        )

        # User can manage bulletins
        cls.user_with_management_access = create_fake_user(
            character_id=random_id(),
            character_name="Clark Kent",
            permissions=[
                "aa_bulletin_board.basic_access",
                "aa_bulletin_board.manage_bulletins",
            ],
        )

    def test_should_show_dashboard(self) -> None:
        """
        Test that a user with basic_access can see the bulletin board

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_with_basic_access)

        # when
        res = self.client.get(path=reverse(viewname="aa_bulletin_board:dashboard"))

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_bulletin(self) -> None:
        """
        Test that a user with basic_access can see the bulletin

        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_without_access,
        )
        self.client.force_login(user=self.user_with_basic_access)

        # when
        res = self.client.get(
            path=reverse(
                viewname="aa_bulletin_board:view_bulletin",
                kwargs={"slug": bulletin.slug},
            )
        )
        result = Bulletin.objects.user_has_access(user=self.user_with_basic_access)

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)
        self.assertIn(member=bulletin, container=result)

    def test_should_not_show_dashboard(self) -> None:
        """
        Test that a user without basic_access can't see the bulletin board

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_without_access)

        # when
        res = self.client.get(path=reverse(viewname="aa_bulletin_board:dashboard"))

        # then
        self.assertIsNot(expr1=res.status_code, expr2=HTTPStatus.OK)

    def test_should_not_show_bulletin(self) -> None:
        """
        Test that a user without basic_access can't see the bulletin

        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_without_access,
        )
        self.client.force_login(user=self.user_without_access)

        # when
        res = self.client.get(
            path=reverse(
                viewname="aa_bulletin_board:view_bulletin",
                kwargs={"slug": bulletin.slug},
            )
        )

        # then
        self.assertIsNot(expr1=res.status_code, expr2=HTTPStatus.OK)

    def test_should_return_bulletin_for_user_with_perm_manage_bulletins(self) -> None:
        """
        Test that a user with "aa_bulletin_board.manage_bulletins" can see all bulletins

        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_without_access,
        )

        # when
        result = Bulletin.objects.user_has_access(user=self.user_with_management_access)

        # then
        self.assertIn(member=bulletin, container=result)

    def test_should_return_restricted_bulletin_for_user_with_perm_manage_bulletins(
        self,
    ) -> None:
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
            created_by=self.user_without_access,
        )
        bulletin.groups.add(self.group)

        # when
        result = Bulletin.objects.user_has_access(user=self.user_with_management_access)

        # then
        self.assertIn(member=bulletin, container=result)

    def test_should_return_bulletin_with_no_groups(self) -> None:
        """
        Test that any user with access can se non-restricted bulletins

        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_without_access,
        )

        # when
        result = Bulletin.objects.user_has_access(user=self.user_with_basic_access)

        # then
        self.assertIn(member=bulletin, container=result)

    def test_should_return_bulletin_for_group_member(self) -> None:
        """
        Test that group restricted bulletins are visible for users who have this group

        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title="Physics",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_without_access,
        )
        bulletin.groups.add(self.group)
        self.user_without_access.groups.add(self.group)

        # when
        result = Bulletin.objects.user_has_access(user=self.user_without_access)

        # then
        self.assertIn(member=bulletin, container=result)

    def test_should_not_return_bulletin_for_non_group_member(self) -> None:
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
            created_by=self.user_with_basic_access,
        )
        bulletin.groups.add(self.group)

        # when
        result = Bulletin.objects.user_has_access(user=self.user_with_basic_access)

        # then
        self.assertNotIn(member=bulletin, container=result)
