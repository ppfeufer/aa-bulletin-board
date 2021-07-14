"""
Forms definition
"""

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from django.forms import ModelForm

from aa_bulletin_board.models import Bulletin


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

    class Meta:
        model = Bulletin
        fields = ["title", "content"]
