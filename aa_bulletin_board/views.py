"""
The views
"""

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# AA Bulletin Board
from aa_bulletin_board.forms import Bulletin, BulletinForm


@login_required
@permission_required("aa_bulletin_board.basic_access")
def dashboard(request):
    """
    Index view
    """

    bulletins = (
        Bulletin.objects.prefetch_related(
            Prefetch("groups", queryset=Group.objects.order_by("name"))
        )
        .user_has_access(request.user)
        .order_by("-created_date")
    )
    context = {"bulletins": bulletins}

    return render(request, "aa_bulletin_board/dashboard.html", context)


@login_required
@permission_required("aa_bulletin_board.manage_bulletins")
def create_bulletin(request):
    """
    Edit an existing bulletin
    :param request:
    :return:
    """

    if request.method == "POST":
        # Create a form instance and populate it with data
        form = BulletinForm(request.POST)

        # Check whether it's valid:
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

            bulletin.groups.set(form.cleaned_data["groups"])

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
        "form": form,
        "bulletin": False,
    }

    return render(request, "aa_bulletin_board/edit-bulletin.html", context)


@login_required
@permission_required("aa_bulletin_board.basic_access")
def view_bulletin(request, slug):
    """
    View a bulletin
    """

    try:
        bulletin = Bulletin.objects.user_has_access(request.user).get(slug=slug)
        context = {"bulletin": bulletin, "slug": slug}

        return render(request, "aa_bulletin_board/bulletin.html", context)
    except Bulletin.DoesNotExist:
        messages.warning(
            request,
            _(
                "The bulletin you are looking for does not exist, "
                "or you don't have access to it."
            ),
        )

        return redirect("aa_bulletin_board:dashboard")


@login_required
@permission_required("aa_bulletin_board.manage_bulletins")
def edit_bulletin(request, slug):
    """
    Edit an existing bulletin
    :param request:
    :param slug:
    :return:
    """

    try:
        bulletin = Bulletin.objects.get(slug=slug)

        if request.method == "POST":
            # Create a form instance and populate it with data
            form = BulletinForm(request.POST, instance=bulletin)

            # Check whether it's valid:
            if form.is_valid():
                bulletin__title = form.cleaned_data["title"]
                bulletin__content = form.cleaned_data["content"]
                bulletin__updated_date = timezone.now()

                bulletin.title = bulletin__title
                bulletin.content = bulletin__content
                bulletin.updated_date = bulletin__updated_date
                bulletin.groups.set(form.cleaned_data["groups"])
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
    Remove bulletin
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
