"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.text import format_lazy

# AA Bulletin Board
from aa_bulletin_board import __title_translated__, __version__


class AaBulletinBoardConfig(AppConfig):
    """
    Application config
    """

    name = "aa_bulletin_board"
    label = "aa_bulletin_board"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
