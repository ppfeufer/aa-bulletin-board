"""
App settings
"""

# Django
from django.conf import settings


def debug_enabled() -> bool:
    """
    Check if DEBUG is enabled

    :return: True if DEBUG is enabled, False otherwise
    :rtype: bool
    """

    return settings.DEBUG
