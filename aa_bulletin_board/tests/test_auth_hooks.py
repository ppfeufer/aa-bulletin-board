"""
Test auth_hooks
"""

# Standard Library
import importlib
import sys
import typing
from http import HTTPStatus

# Django
from django.urls import reverse

# AA Bulletin Board
from aa_bulletin_board.tests import BaseTestCase
from aa_bulletin_board.tests.utils import create_fake_user, random_id


class TestHooks(BaseTestCase):
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
        cls.user_without_access = create_fake_user(
            character_id=random_id(), character_name="Peter Parker"
        )

        # User can access bulletins
        cls.user_with_basic_access = create_fake_user(
            character_id=random_id(),
            character_name="Bruce Wayne",
            permissions=["aa_bulletin_board.basic_access"],
        )

        cls.html_menu = f"""
            <li class="d-flex flex-wrap m-2 p-2 pt-0 pb-0 mt-0 mb-0 me-0 pe-0">
                <i class="nav-link fa-solid fa-clipboard-list fa-fw align-self-center me-3 "></i>
                <a class="nav-link flex-fill align-self-center me-auto" href="{reverse(viewname='aa_bulletin_board:dashboard')}">
                    Bulletin Board
                </a>
            </li>
        """

    def login(self, user):
        """
        Login a test user

        :param user:
        :type user:
        :return:
        :rtype:
        """

        self.client.force_login(user=user)

    def test_render_hook_success(self) -> None:
        """
        Test should show the link to the app in the navigation to user with access

        :return:
        :rtype:
        """

        self.login(user=self.user_with_basic_access)

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

        self.login(user=self.user_without_access)

        response = self.client.get(path=reverse(viewname="authentication:dashboard"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, self.html_menu, html=True)

    def test_type_checking_block_imports_wsgi_request_when_enabled(self):
        """
        Ensure that when typing.TYPE_CHECKING is True at import time the
        module-level name `WSGIRequest` is present in the `auth_hooks`
        module namespace.

        :return:
        """

        module_name = "aa_bulletin_board.auth_hooks"
        orig_module = sys.modules.get(module_name)
        orig_flag = typing.TYPE_CHECKING

        try:
            # Ensure django is available for this check, otherwise skip.
            try:
                # Django
                import django.core.handlers.wsgi  # noqa: F401
            except Exception:
                self.skipTest("Django WSGIRequest unavailable in this environment")

            if module_name in sys.modules:
                del sys.modules[module_name]

            typing.TYPE_CHECKING = True
            mod = importlib.import_module(module_name)

            self.assertTrue(hasattr(mod, "WSGIRequest"))
        finally:
            typing.TYPE_CHECKING = orig_flag
            if orig_module is not None:
                sys.modules[module_name] = orig_module
            else:
                sys.modules.pop(module_name, None)

    def test_type_checking_block_does_not_import_wsgi_request_when_disabled(self):
        """
        Ensure that when typing.TYPE_CHECKING is False at import time the
        module-level name `WSGIRequest` is not present in the `auth_hooks`
        module namespace.

        :return:
        """

        module_name = "aa_bulletin_board.auth_hooks"
        orig_module = sys.modules.get(module_name)
        orig_flag = typing.TYPE_CHECKING

        try:
            if module_name in sys.modules:
                del sys.modules[module_name]

            typing.TYPE_CHECKING = False
            mod = importlib.import_module(module_name)

            self.assertFalse(hasattr(mod, "WSGIRequest"))
        finally:
            typing.TYPE_CHECKING = orig_flag
            if orig_module is not None:
                sys.modules[module_name] = orig_module
            else:
                sys.modules.pop(module_name, None)
