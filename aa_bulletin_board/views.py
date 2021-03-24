"""
the views
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from aa_bulletin_board.app_settings import avoid_cdn
from aa_bulletin_board.forms import Bulletin, BulletinForm


@login_required
@permission_required("aa_bulletin_board.basic_access")
def dashboard(request):
    """
    index view
    """

    bulletins = Bulletin.objects.all().order_by("-created_date")
    context = {"avoidCdn": avoid_cdn(), "bulletins": bulletins}

    return render(request, "aa_bulletin_board/dashboard.html", context)


@login_required
@permission_required("aa_bulletin_board.manage_bulletins")
def create_bulletin(request):
    """
    edit an existing bulletin
    :param request:
    :return:
    """

    if request.method == "POST":
        # create a form instance and populate it with data
        form = BulletinForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            bulletin__title = form.cleaned_data["title"]
            bulletin__content = form.cleaned_data["content"]
            bulletin__created_date = timezone.now()

            bulletin = Bulletin()
            bulletin.title = bulletin__title
            bulletin.content = bulletin__content
            bulletin.created_date = bulletin__created_date
            bulletin.created_by = request.user
            bulletin.save()

            messages.success(
                request,
                _('Bulletin "{bulletin_title}" created').format(
                    bulletin_title=bulletin__title
                ),
            )

            return redirect("aa_bulletin_board:view_bulletin", bulletin.slug)
    else:
        form = BulletinForm()

    context = {
        "avoidCdn": avoid_cdn(),
        "form": form,
        "bulletin": False,
    }

    return render(request, "aa_bulletin_board/edit-bulletin.html", context)


@login_required
@permission_required("aa_bulletin_board.basic_access")
def view_bulletin(request, slug):
    """
    view a bulletin
    """

    try:
        bulletin = Bulletin.objects.get(slug=slug)
        context = {"avoidCdn": avoid_cdn(), "bulletin": bulletin, "slug": slug}

        return render(request, "aa_bulletin_board/bulletin.html", context)
    except Bulletin.DoesNotExist:
        messages.warning(
            request,
            _("The bulletin you are looking for does not exist."),
        )

        return redirect("aa_bulletin_board:dashboard")


@login_required
@permission_required("aa_bulletin_board.manage_bulletins")
def edit_bulletin(request, slug):
    """
    edit an existing bulletin
    :param request:
    :param slug:
    :return:
    """

    try:
        bulletin = Bulletin.objects.get(slug=slug)

        if request.method == "POST":
            # create a form instance and populate it with data
            form = BulletinForm(request.POST, instance=bulletin)

            # check whether it's valid:
            if form.is_valid():
                bulletin__title = form.cleaned_data["title"]
                bulletin__content = form.cleaned_data["content"]
                bulletin__updated_date = timezone.now()

                bulletin.title = bulletin__title
                bulletin.content = bulletin__content
                bulletin.updated_date = bulletin__updated_date
                bulletin.save()

                messages.success(
                    request,
                    _('Bulletin "{bulletin_title}" updated').format(
                        bulletin_title=bulletin__title
                    ),
                )

                return redirect("aa_bulletin_board:view_bulletin", bulletin.slug)
        else:
            form = BulletinForm(instance=bulletin)

        context = {
            "avoidCdn": avoid_cdn(),
            "form": form,
            "existing_bulletin": True,
            "bulletin": bulletin,
        }

        return render(request, "aa_bulletin_board/edit-bulletin.html", context)
    except Bulletin.DoesNotExist:
        messages.warning(
            request,
            _("The bulletin you are trying to edit for does not exist."),
        )

        return redirect("aa_bulletin_board:dashboard")


@login_required
@permission_required("aa_bulletin_board.manage_bulletins")
def remove_bulletin(request, slug):
    """
    remove bulletin
    :param request:
    :param slug:
    :return:
    """

    try:
        bulletin = Bulletin.objects.get(slug=slug)

        messages.success(
            request,
            _('Bulletin "{bulletin_title}" deleted.').format(
                bulletin_title=bulletin.title
            ),
        )

        bulletin.delete()
    except Bulletin.DoesNotExist:
        messages.warning(
            request,
            _("The bulletin you are trying to delete for does not exist."),
        )

    return redirect("aa_bulletin_board:dashboard")
