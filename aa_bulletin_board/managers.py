"""
Managers for our models
"""

# Django
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class BulletinQuerySet(models.QuerySet):
    def user_has_access(self, user: User) -> models.QuerySet:
        """
        Filter boards that given user has access to.
        """

        # Forum manager have always access, so assign this permission wisely
        if user.has_perm("aa_bulletin_board.manage_bulletins"):
            return self

        # If not a forum manager, check if the user has access to the board
        return self.filter(
            Q(groups__in=user.groups.all()) | Q(groups__isnull=True)
        ).distinct()


class BulletinManagerBase(models.Manager):
    """
    BoardManagerBase
    """

    pass


BulletinManager = BulletinManagerBase.from_queryset(BulletinQuerySet)
