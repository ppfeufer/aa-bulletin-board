"""
Helper functions for static integrity calculations
"""

# Standard Library
import os
from pathlib import Path

# Third Party
from sri import Algorithm, calculate_integrity

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Bulletin Board
from aa_bulletin_board import __title__
from aa_bulletin_board.constants import APP_STATIC_DIR

logger = LoggerAddTag(my_logger=get_extension_logger(__name__), prefix=__title__)


def calculate_integrity_hash(relative_file_path: str) -> str:
    """
    Calculates the integrity hash for a given static file

    :param self:
    :type self:
    :param relative_file_path: The file path relative to the `{APP_NAME}/{PACKAGE_NAME}/static/{PACKAGE_NAME}` folder
    :type relative_file_path: str
    :return: The integrity hash
    :rtype: str
    """

    return calculate_integrity(
        path=Path(os.path.join(APP_STATIC_DIR, relative_file_path)),
        algorithm=Algorithm.SHA512,
    )
