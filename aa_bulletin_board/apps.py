"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# AA Bulletin Board
from aa_bulletin_board import __version__


class AaBulletinBoardConfig(AppConfig):
    """
    Application config
    """

    name = "aa_bulletin_board"
    label = "aa_bulletin_board"
    # Translators: This is the app name and version, which will appear in the Django Backend
    verbose_name = _(f"Bulletin Board v{__version__}")
