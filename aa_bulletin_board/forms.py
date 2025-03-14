"""
Forms definition
"""

# Django
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

# CKEditor
from django_ckeditor_5.widgets import CKEditor5Widget

# AA Bulletin Board
from aa_bulletin_board.helper.string import string_cleanup
from aa_bulletin_board.models import Bulletin


class SpecialModelChoiceIterator(forms.models.ModelChoiceIterator):
    """
    Variant of Django's ModelChoiceIterator to prevent it from always re-fetching the
    given queryset from the database.
    """

    def __iter__(self):
        if self.field.empty_label is not None:
            yield "", self.field.empty_label

        queryset = self.queryset

        for obj in queryset:
            yield self.choice(obj=obj)


class SpecialModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Variant of Django's ModelMultipleChoiceField to prevent it from always
    re-fetching the given queryset from the database.
    """

    iterator = SpecialModelChoiceIterator

    def _get_queryset(self):
        return self._queryset

    def _set_queryset(self, queryset):
        self._queryset = queryset
        self.widget.choices = self.choices

    queryset = property(fget=_get_queryset, fset=_set_queryset)


class BulletinForm(ModelForm):
    """
    Form for bulletins
    """

    groups = SpecialModelMultipleChoiceField(
        required=False,
        queryset=Group.objects.all(),
        help_text=_(
            "Restrict this bulletin to certain groups. "
            "If no group restrictions are in place, everyone who has access to "
            "this module can read this bulletin."
        ),
    )

    def __init__(self, *args, **kwargs):
        groups_queryset = kwargs.pop("groups_queryset", None)

        super().__init__(*args, **kwargs)

        if groups_queryset:
            self.fields["groups"].queryset = groups_queryset

        # We have to set this to False, otherwise CKEditor5 will not work
        self.fields["content"].required = False

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Form Meta
        """

        model = Bulletin
        fields = ["title", "content", "groups"]
        widgets = {
            "content": CKEditor5Widget(
                config_name="extends",
                attrs={
                    "class": "aa-bulletin-board-ckeditor django_ckeditor_5",
                    "rows": 10,
                    "cols": 20,
                    "style": "width: 100%;",
                },
            )
        }

    def clean(self):
        """
        Clean the form

        :return:
        :rtype:
        """

        cleaned_data = super().clean()
        content = cleaned_data.get("content")

        if not content or content.strip() == "":
            self.add_error(
                "content", ValidationError(_("You have forgotten the content!"))
            )

        cleaned_data["content"] = content.strip()

        return cleaned_data

    def clean_content(self) -> str:
        """
        Cleanup the content

        :return:
        :rtype:
        """

        content = string_cleanup(string=self.cleaned_data["content"])

        return content
