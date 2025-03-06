"""
Test the apps' template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase, override_settings

# AA Bulletin Board
from aa_bulletin_board import __version__
from aa_bulletin_board.constants import PACKAGE_NAME
from aa_bulletin_board.helper.static_files import calculate_integrity_hash


class TestVersionedStatic(TestCase):
    """
    Test aa_bulletin_board_static template tag
    """

    @override_settings(DEBUG=False)
    def test_versioned_static_without_debug_enabled(self) -> None:
        """
        Test versioned static template tag without DEBUG enabled

        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load aa_bulletin_board %}"
                "{% aa_bulletin_board_static 'css/aa-bulletin-board.min.css' %}"
                "{% aa_bulletin_board_static 'javascript/aa-bulletin-board-oembed.min.js' %}"
            )
        )

        rendered_template = template_to_render.render(context=context)

        expected_static_css_src = f'/static/{PACKAGE_NAME}/css/aa-bulletin-board.min.css?v={context["version"]}'
        expected_static_css_src_integrity = calculate_integrity_hash(
            "css/aa-bulletin-board.min.css"
        )
        expected_static_js_src = f'/static/{PACKAGE_NAME}/javascript/aa-bulletin-board-oembed.min.js?v={context["version"]}'
        expected_static_js_src_integrity = calculate_integrity_hash(
            "javascript/aa-bulletin-board-oembed.min.js"
        )

        self.assertIn(member=expected_static_css_src, container=rendered_template)
        self.assertIn(
            member=expected_static_css_src_integrity, container=rendered_template
        )
        self.assertIn(member=expected_static_js_src, container=rendered_template)
        self.assertIn(
            member=expected_static_js_src_integrity, container=rendered_template
        )

    @override_settings(DEBUG=True)
    def test_versioned_static_with_debug_enabled(self) -> None:
        """
        Test versioned static template tag with DEBUG enabled

        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load aa_bulletin_board %}"
                "{% aa_bulletin_board_static 'css/aa-bulletin-board.min.css' %}"
            )
        )

        rendered_template = template_to_render.render(context=context)

        expected_static_css_src = f'/static/{PACKAGE_NAME}/css/aa-bulletin-board.min.css?v={context["version"]}'

        self.assertIn(member=expected_static_css_src, container=rendered_template)
        self.assertNotIn(member="integrity=", container=rendered_template)

    def test_invalid_file_type(self) -> None:
        """
        Test should raise a ValueError for an invalid file type

        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load aa_bulletin_board %}"
                "{% aa_bulletin_board_static 'invalid/invalid.txt' %}"
            )
        )

        with self.assertRaises(ValueError):
            template_to_render.render(context=context)
