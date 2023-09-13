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

    re_head = re.compile(
        pattern=r"<\s*head[^>]*>.*?<\s*/\s*head\s*>", flags=re.S | re.I
    )
    re_script = re.compile(
        pattern=r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", flags=re.S | re.I
    )
    re_css = re.compile(
        pattern=r"<\s*style[^>]*>.*?<\s*/\s*style\s*>", flags=re.S | re.I
    )

    # Strip unwanted content (JS, CSS, HTML-Head)
    string = re_head.sub(repl="", string=string)
    string = re_script.sub(repl="", string=string)
    string = re_css.sub(repl="", string=string)

    return string
