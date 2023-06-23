"""
Forms definition
"""

# Django
from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

# ckEditor
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# AA Bulletin Board
from aa_bulletin_board.helpers import string_cleanup
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
            yield self.choice(obj)


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

    queryset = property(_get_queryset, _set_queryset)


class BulletinForm(ModelForm):
    """
    Form for bulletins
    """

    title = forms.CharField()

    content = forms.CharField(
        widget=CKEditorUploadingWidget(
            config_name="aa_bulletin_board",
            attrs={"rows": 10, "cols": 20, "style": "width: 100%;"},
        )
    )

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

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Form Meta
        """

        model = Bulletin
        fields = ["title", "content", "groups"]

    def clean_content(self):
        """
        Cleanup the content
        :return:
        """

        message = string_cleanup(self.cleaned_data["content"])

        return message
