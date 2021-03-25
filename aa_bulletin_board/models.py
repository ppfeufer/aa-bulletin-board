"""
the models
"""

from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _


def get_sentinel_user() -> User:
    """
    get user or create one
    :return:
    """

    return User.objects.get_or_create(username="deleted")[0]


def get_bulletin_slug_from_title(bulletin_title: str) -> str:
    """
    get the slug from the title
    :param bulletin_title:
    :return:
    """

    run = 0
    bulletin_slug = slugify(bulletin_title, allow_unicode=True)

    while Bulletin.objects.filter(slug=bulletin_slug).exists():
        run += 1
        bulletin_slug = slugify(bulletin_title + "-" + str(run), allow_unicode=True)

    return bulletin_slug


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        verbose_name = "Bulletins"
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access this app"),
            ("manage_bulletins", "Can manage (add/change/remove) bulletins"),
        )


class Bulletin(models.Model):
    """
    Bulletin model
    """

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    content = RichTextUploadingField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET(get_sentinel_user),
    )

    class Meta:
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Bulletin")
        verbose_name_plural = _("Bulletins")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        add the slug on save
        """

        if self.slug == "":
            bulletin_slug = get_bulletin_slug_from_title(bulletin_title=self.title)
            self.slug = bulletin_slug

        super().save()
