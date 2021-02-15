"""
the views
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from aa_bulletin_board.app_settings import avoid_cdn
from aa_bulletin_board.models import Bulletin


@login_required
@permission_required("aa_bulletin_board.basic_access")
def dashboard(request):
    """
    Index view
    """

    try:
        bulletins = Bulletin.objects.all()
    except Bulletin.DoesNotExist:
        bulletins = None

    context = {"avoidCdn": avoid_cdn(), "bulletins": bulletins}

    return render(request, "aa_bulletin_board/dashboard.html", context)


@login_required
@permission_required("aa_bulletin_board.basic_access")
def view_bulletin(request, slug):
    """
    Index view
    """

    try:
        bulletin = Bulletin.objects.get(slug=slug)
    except Bulletin.DoesNotExist:
        bulletin = None

    context = {"avoidCdn": avoid_cdn(), "bulletin": bulletin, "slug": slug}

    return render(request, "aa_bulletin_board/bulletin.html", context)
