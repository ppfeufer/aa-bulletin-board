"""
Constants used in this app
"""

# Standard Library
import os

# Django
from django.utils.translation import gettext_lazy as _

APP_NAME = "aa-bulletin-board"
APP_NAME_VERBOSE = "AA Bulletin Board"
APP_TITLE = _("Bulletin Board")
PACKAGE_NAME = "aa_bulletin_board"
APP_BASE_DIR = os.path.join(os.path.dirname(__file__))
APP_STATIC_DIR = os.path.join(APP_BASE_DIR, "static", PACKAGE_NAME)
GITHUB_URL = f"https://github.com/ppfeufer/{APP_NAME}"
