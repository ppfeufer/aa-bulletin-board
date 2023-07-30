"""
App init
"""

# Standard Library
from importlib import metadata

# Django
from django.utils.translation import gettext_lazy as _

__version__ = metadata.version("aa-bulletin-board")
__title__ = _("Bulletin Board")

del metadata
