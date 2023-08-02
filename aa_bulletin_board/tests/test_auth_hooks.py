"""
Test auth_hooks
"""

# Standard Library
from http import HTTPStatus

# Django
from django.test import TestCase
from django.urls import reverse

# AA Bulletin Board
from aa_bulletin_board.tests.utils import create_fake_user


class TestHooks(TestCase):
    """
    Test the app hook into allianceauth
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users

        :return:
        :rtype:
        """

        super().setUpClass()

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

        cls.html_menu = f"""
            <li>
                <a class href="{reverse(viewname='aa_bulletin_board:dashboard')}">
                    <i class="fas fa-clipboard-list fa-fw"></i> Bulletin Board
                </a>
            </li>
        """

    def test_render_hook_success(self) -> None:
        """
        Test should show the link to the app in the navigation to user with access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1002)

        response = self.client.get(path=reverse(viewname="authentication:dashboard"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.html_menu, html=True)

    def test_render_hook_fail(self) -> None:
        """
        Test should not show the link to the app in the
        navigation to user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1001)

        response = self.client.get(path=reverse(viewname="authentication:dashboard"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, self.html_menu, html=True)
