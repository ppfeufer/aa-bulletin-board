"""
App config
"""

# Django
from django.apps import AppConfig

# AA Bulletin Board
from aa_bulletin_board import __version__


class AaBulletinBoardConfig(AppConfig):
    """
    Application config
    """

    name = "aa_bulletin_board"
    label = "aa_bulletin_board"
    verbose_name = f"Bulletin Board v{__version__}"
