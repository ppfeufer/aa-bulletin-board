"""
Hook into AA
"""

__lazy_modules__ = ["django.core.handlers.wsgi"]

# Standard Library
from typing import TYPE_CHECKING

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Bulletin Board
from aa_bulletin_board import __title_translated__, urls

if TYPE_CHECKING:
    # Django
    from django.core.handlers.wsgi import WSGIRequest


class AaBulletinBoardMenuItem(MenuItemHook):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self):
        """
        Setup menu entry for sidebar
        """

        MenuItemHook.__init__(
            self,
            text=__title_translated__,
            classes="fa-solid fa-clipboard-list",
            url_name="aa_bulletin_board:dashboard",
            navactive=["aa_bulletin_board:"],
        )

    def render(self, request: "WSGIRequest") -> str:
        """
        Check if the user has the permission to view this app

        :param request: WSGI request
        :type request: WSGIRequest
        :return: Rendered menu item or empty string
        :rtype: str
        """

        return (
            MenuItemHook.render(self, request=request)
            if request.user.has_perm("aa_bulletin_board.basic_access")
            else ""
        )


@hooks.register("menu_item_hook")
def register_menu():
    """
    Register our menu item

    :return: Menu item hook
    :rtype: AaBulletinBoardMenuItem
    """

    return AaBulletinBoardMenuItem()


@hooks.register("url_hook")
def register_urls() -> UrlHook:
    """
    Register our base url

    :return: URL hook
    :rtype: UrlHook
    """

    return UrlHook(
        urls=urls, namespace="aa_bulletin_board", base_url=r"^bulletin-board/"
    )
