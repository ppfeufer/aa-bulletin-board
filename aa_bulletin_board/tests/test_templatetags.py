"""
Test the apps' template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# AA Bulletin Board
from aa_bulletin_board import __version__


class TestVersionedStatic(TestCase):
    def test_versioned_static(self):
        context = Context({"version": __version__})
        template_to_render = Template(
            "{% load aa_bulletin_board_versioned_static %}"
            "{% aa_bulletin_board_static 'aa_bulletin_board/css/aa-bulletin-board.min.css' %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertInHTML(
            f'/static/aa_bulletin_board/css/aa-bulletin-board.min.css?v={context["version"]}',
            rendered_template,
        )
