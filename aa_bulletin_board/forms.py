from aa_bulletin_board.models import Bulletin

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.forms import ModelForm


class BulletinForm(ModelForm):
    """
    form for bulletins
    """

    title = forms.CharField()

    content = forms.CharField(
        widget=CKEditorWidget(attrs={"rows": 10, "cols": 20, "style": "width: 100%;"})
    )

    class Meta:
        model = Bulletin
        fields = ["title", "content"]
