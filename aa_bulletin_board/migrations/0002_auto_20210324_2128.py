# Generated by Django 3.1.7 on 2021-03-24 21:28

import ckeditor_uploader.fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aa_bulletin_board", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bulletin",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, null=True
            ),
        ),
    ]
