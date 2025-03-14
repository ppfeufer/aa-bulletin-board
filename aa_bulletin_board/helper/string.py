"""
Our little helpers
"""

# Standard Library
import re


def string_cleanup(string: str) -> str:
    """
    Clean up a string by removing JS, CSS and Head tags

    :param string:
    :type string:
    :return:
    :rtype:
    """

    # Strip unwanted content (JS, CSS, HTML-Head)
    return re.compile(
        pattern=r"<\s*(head|script|style)[^>]*>.*?<\s*/\s*\1\s*>", flags=re.S | re.I
    ).sub(repl="", string=string)
