from django.shortcuts import render
from django.conf import settings
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from generic_confirmation.forms import ConfirmationForm

from ajaxutils.decorators import ajax

from .forms import MemberForm, MemberEmailForm
from .models import Member

from dotmembership.apps.billing.models import Invoice


def index(request):
    """
    Index page of the member register.

    Renders a page which contains forms for joining and
    sending a self edit link
    """
    member_form = MemberForm()
    email_form = MemberEmailForm()

    return render(request, 'index.html', {'member_form': member_form,
        'email_form': email_form})


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


@ajax(require_POST=True)
def send_edit_link(request):
    """
    AJAX view for sending member edit link in email.
    """
    form = MemberEmailForm(request.POST)

    if form.is_valid():
        instance = form.save(commit=False)
        try:
            member = Member.objects.get(email=instance.email)
            member.send_edit_link()
        except Member.DoesNotExist:
            pass

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
            member = Member.objects.get(pk=request.GET.get("member_id"))
        else:
            member = form.save()

        if member:
            fields = Member.PUBLIC_FIELDS

            # Pass form in to show the user data that was submitted
            # The invoice shown here is the one that is created in post_save
            context = {"fields": fields,
                       "member": member,
                       "invoice": member.invoices.get(status=Invoice.STATUS.sent)}
            return render(request, "members/confirm_join_success.html", context)

    return render(request, "members/confirm_join_error.html")


def edit(request, signed_id):
    signer = TimestampSigner()
    try:
        signer.unsign(signed_id, max_age=10)
    except (BadSignature, SignatureExpired):
        return render(request, "members/edit_failed.html")

    if request.method == "POST":
        pass

    return render(request, "members/edit.html")


def check_my_data(request):
    pass
