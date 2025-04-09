"""
The models
"""

# Standard Library
from typing import ClassVar

# Third Party
import unidecode

# Django
from django.contrib.auth.models import Group, User
from django.db import models, transaction
from django.utils.text import slugify
from django.utils.translation import gettext as _

# CKEditor
from django_ckeditor_5.fields import CKEditor5Field

# AA Bulletin Board
from aa_bulletin_board.constants import APP_TITLE
from aa_bulletin_board.helper.string import string_cleanup
from aa_bulletin_board.managers import BulletinManager


def get_sentinel_user() -> User:
    """
    Get the sentinel user or create one

    :return:
    :rtype:
    """

    return User.objects.get_or_create(username="deleted")[0]


def get_bulletin_slug_from_title(bulletin_title: str) -> str:
    """
    Get the slug from the title

    :param bulletin_title:
    :type bulletin_title:
    :return:
    :rtype:
    """

    base_slug = slugify(value=unidecode.unidecode(bulletin_title), allow_unicode=True)
    bulletin_slug = base_slug
    run = 0

    while Bulletin.objects.filter(slug=bulletin_slug).exists():
        run += 1
        bulletin_slug = f"{base_slug}-{run}"

    return bulletin_slug


class General(models.Model):
    """
    Meta model for app permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        verbose_name = APP_TITLE
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", _("Can access this app")),
            ("manage_bulletins", _("Can manage (add/change/remove) bulletins")),
        )


class Bulletin(models.Model):
    """
    Bulletin model
    """

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    content = CKEditor5Field(
        blank=False, default=None, verbose_name=_("Content"), config_name="extends"
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        # Translators: This is the date and time the bulletin has been created
        verbose_name=_("Created"),
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        null=True,
        # Translators: This is the date and time the bulletin has been updated
        verbose_name=_("Updated"),
    )
    created_by = models.ForeignKey(
        to=User,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET(get_sentinel_user),
        verbose_name=_("User"),
    )
    groups = models.ManyToManyField(
        to=Group,
        blank=True,
        related_name="aa_bulletin_board_group_restriction",
        verbose_name=_("Group restrictions"),
    )

    objects: ClassVar[BulletinManager] = BulletinManager()

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Bulletin")
        verbose_name_plural = _("Bulletins")

    def __str__(self) -> str:
        return str(self.title)

    @transaction.atomic()
    def save(self, *args, **kwargs) -> None:
        """
        Add the slug on save

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        self.content = string_cleanup(string=self.content)

        if not self.slug:
            self.slug = get_bulletin_slug_from_title(bulletin_title=self.title)

        super().save(*args, **kwargs)
