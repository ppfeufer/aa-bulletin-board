"""
Test for aa_bulletin_board.forms
"""

# Django
from django.contrib.auth.models import Group
from django.test import TestCase

# AA Bulletin Board
from aa_bulletin_board.forms import (
    BulletinForm,
    SpecialModelChoiceIterator,
    SpecialModelMultipleChoiceField,
)


class TestSpecialModelChoiceIterator(TestCase):
    """
    Tests for SpecialModelChoiceIterator
    """

    def test_iterates_over_queryset(self):
        """
        Test iterates over the queryset without re-fetching it

        :return:
        :rtype:
        """

        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")

        field = SpecialModelMultipleChoiceField(queryset=Group.objects.all())
        iterator = SpecialModelChoiceIterator(field)

        choices = list(iterator)

        self.assertIn((group1.pk, str(group1)), choices)
        self.assertIn((group2.pk, str(group2)), choices)

    def test_includes_empty_label_if_set(self):
        """
        Test includes empty label if a label is set

        :return:
        :rtype:
        """

        field = SpecialModelMultipleChoiceField(queryset=Group.objects.all())
        field.empty_label = "Select a group"
        iterator = SpecialModelChoiceIterator(field)

        choices = list(iterator)

        self.assertIn(("", "Select a group"), choices)


class TestSpecialModelMultipleChoiceField(TestCase):
    """
    Tests for SpecialModelMultipleChoiceField
    """

    def test_sets_and_gets_queryset(self):
        """
        Test sets and gets the queryset without re-fetching it

        :return:
        :rtype:
        """

        field = SpecialModelMultipleChoiceField(queryset=Group.objects.none())
        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")
        field.queryset = Group.objects.all()

        self.assertEqual(list(field.queryset), [group1, group2])

    def test_updates_widget_choices_when_queryset_is_set(self):
        """
        Test updates the widget choices when the queryset is set

        :return:
        :rtype:
        """

        field = SpecialModelMultipleChoiceField(queryset=Group.objects.none())
        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")
        field.queryset = Group.objects.all()

        self.assertIn((group1.pk, str(group1)), field.widget.choices)
        self.assertIn((group2.pk, str(group2)), field.widget.choices)

    def test_handles_empty_queryset(self):
        """
        Test handles empty queryset

        :return:
        :rtype:
        """

        field = SpecialModelMultipleChoiceField(queryset=Group.objects.none())

        self.assertEqual(list(field.queryset), [])
        self.assertEqual(list(field.widget.choices), [])


class TestBulletinForm(TestCase):
    """
    Tests for BulletinForm
    """

    def test_valid_form_with_groups_queryset(self):
        """
        Test valid form with groups queryset

        :return:
        :rtype:
        """

        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")
        form_data = {
            "title": "Test Bulletin",
            "content": "This is a test bulletin.",
            "groups": [group1.pk, group2.pk],
        }
        form = BulletinForm(data=form_data, groups_queryset=Group.objects.all())

        self.assertTrue(form.is_valid())

    def test_invalid_form_without_title(self):
        """
        Test invalid form without title

        :return:
        :rtype:
        """

        form_data = {
            "title": "",
            "content": "This is a test bulletin.",
        }
        form = BulletinForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_clean_raises_validation_error_for_empty_content(self):
        """
        Test clean raises validation error for empty content

        :return:
        :rtype:
        """

        form_data = {
            "title": "Test Bulletin",
            "content": "   ",
        }
        form = BulletinForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_clean_content_strips_unwanted_characters(self):
        """
        Test clean content strips unwanted characters

        :return:
        :rtype:
        """

        form_data = {
            "title": "Test Bulletin",
            "content": "  <p>Test content</p>  ",
        }
        form = BulletinForm(data=form_data)
        form.is_valid()

        self.assertEqual(form.cleaned_data["content"], "<p>Test content</p>")
