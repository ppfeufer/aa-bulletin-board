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
    """

    re_head = re.compile(r"<\s*head[^>]*>.*?<\s*/\s*head\s*>", re.S | re.I)
    re_script = re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.S | re.I)
    re_css = re.compile(r"<\s*style[^>]*>.*?<\s*/\s*style\s*>", re.S | re.I)

    # Strip JS
    string = re_head.sub("", string)
    string = re_script.sub("", string)
    string = re_css.sub("", string)

    return string
