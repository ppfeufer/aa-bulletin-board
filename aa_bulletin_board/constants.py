"""
constants used in this app
"""

from django.utils.text import slugify

from aa_bulletin_board import __version__

VERBOSE_NAME = "Bulletin Board for Alliance Auth"
USER_AGENT = "{verbose_name} v{version} {github_url}".format(
    verbose_name=slugify(VERBOSE_NAME, allow_unicode=True),
    version=__version__,
    github_url="https://github.com/ppfeufer/aa-esi-status",
)
