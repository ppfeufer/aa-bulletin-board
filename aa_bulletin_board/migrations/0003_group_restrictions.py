# Generated by Django 3.2.6 on 2021-08-25 08:56

# Django
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("aa_bulletin_board", "0002_alter_bulletin_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="bulletin",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="aa_bulletin_board_group_restriction",
                to="auth.Group",
            ),
        ),
        migrations.AlterField(
            model_name="bulletin",
            name="created_date",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="bulletin",
            name="updated_date",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
