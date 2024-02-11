"""
Test the apps' template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# AA Bulletin Board
from aa_bulletin_board import __version__


class TestVersionedStatic(TestCase):
    """
    Test aa_bulletin_board_static template tag
    """

    def test_versioned_static(self) -> None:
        """
        Test versioned static template tag

        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load aa_bulletin_board %}"
                "{% aa_bulletin_board_static 'aa_bulletin_board/css/aa-bulletin-board.min.css' %}"  # pylint: disable=line-too-long
            )
        )

        rendered_template = template_to_render.render(context=context)

        self.assertInHTML(
            needle=f'/static/aa_bulletin_board/css/aa-bulletin-board.min.css?v={context["version"]}',  # pylint: disable=line-too-long
            haystack=rendered_template,
        )
