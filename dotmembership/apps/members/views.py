from django.shortcuts import render
from django.conf import settings

from generic_confirmation.forms import ConfirmationForm

from ajaxutils.decorators import ajax

from .forms import MemberForm


def index(request):
    """
    Index page of the member register.

    Renders a page which contains forms.
    """
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MemberForm()

    return render(request, 'index.html', {'member_form': form})


@ajax(require_POST=True)
def join(request):
    """
    AJAX view for adding a new member to registry.
    """
    form = MemberForm(request.POST)

    if form.is_valid():
        form.save()
        return {'status': 'success'}

    return {'status': 'error', 'errors': form.errors}


def confirm_join(request, token):
    """
    This view does basically the same as generic_confirmation.views.confirm_by_get,
    but as it didn't allow enough customizations to be made, the view is partia
    copied here and the behavior customized.
    """
    form = ConfirmationForm({'token': token})
    if form.is_valid() or (settings.DEBUG and request.GET.get("member_id")):
        # ConfirmationForm.save returns either the object
        # or False, if the token was not found in the database (I guess
        # this is a bug, since is_valid() should not return True if token
        # cannot be found)
        #from .models import Member
        #member = Member.objects.get(pk=1)
        if settings.DEBUG and request.GET.get("member_id"):
            from .models import Member
            member = Member.objects.get(pk=request.GET.get("member_id"))
        else:
            member = form.save()
        if member:
            fields = MemberForm._meta.fields

            # Pass form in to show the user data that was submitted
            context = {"token_valid": True,
                       "fields": fields,
                       "member": member}
            return render(request, "members/confirm_join.html", context)

    return render(request, "members/confirm_join.html", {"token_valid": False})


def check_my_data(request):
    pass
