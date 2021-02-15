"""
app config
"""

from django.apps import AppConfig

from aa_bulletin_board import __version__


class AaBulletinBoardConfig(AppConfig):
    """
    application config
    """

    name = "aa_bulletin_board"
    label = "aa_bulletin_board"
    verbose_name = "ESI Statusv{}".format(__version__)
