# encoding: utf-8
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.contrib import messages

from generic_confirmation.forms import ConfirmationForm
from django_mailman.models import List

from ajaxutils.decorators import ajax
import datetime

from .forms import MemberForm, EmailForm, MemberJoinForm, MemberEmailEditForm
from .models import Member

from dotmembership.apps.billing.models import Invoice


def index(request):
    """
    Index page of the member register.

    Renders a page which contains forms for joining and
    sending a self edit link
    """
    member_form = MemberJoinForm()
    email_form = EmailForm()

    return render(request, 'index.html', {'member_form': member_form,
        'email_form': email_form})


def mailing_list(request):
    email_form = EmailForm()

    if request.method == "POST":
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            # Join user
            list = List(name=settings.MAILMAN_LIST_NAME,
                        password=settings.MAILMAN_LIST_PASSWORD,
                        email=settings.MAILMAN_LIST_EMAIL,
                        main_url=settings.MAILMAN_MAIN_URL,
                        encoding=settings.MAILMAN_ENCODING)
            try:
                list.subscribe(email=email_form.cleaned_data['email'])
            except Exception as e:
                # django_mailman doesn't define it's own exceptions,
                # so we must identify by the args.
                if email_form.cleaned_data['email'] in str(e):
                    messages.error(request, u"Olet jo liittynyt listallemme.")
                else:
                    # Unknown, let it bubble
                    raise
            else:
                messages.success(request, u"Onnittelut, sähköpostiosoitteesi %s on nyt liitetty listalle!" % (email_form.cleaned_data['email'],))
                return HttpResponseRedirect(request.get_full_path())
            # send email
    else:
        email_form = EmailForm()

    email_form.fields['email'].help_text = u"Syötä sähköpostiosoite, jolla haluat liittyä listalle."

    return render(request, "members/join_mailing_list.html", {'email_form': email_form})


@ajax(require_POST=True)
def join(request):
    """
    AJAX view for adding a new member to registry.
    """
    form = MemberJoinForm(request.POST)

    if form.is_valid():
        form.save()
        return {'status': 'success'}

    return {'status': 'error', 'errors': form.errors}


@ajax(require_POST=True)
def send_edit_link(request):
    """
    AJAX view for sending member edit link in email.
    """
    form = EmailForm(request.POST)

    if form.is_valid():
        try:
            member = Member.objects.get(email=form.cleaned_data["email"])
            member.send_data_and_edit_link()
        except Member.DoesNotExist:
            return {'status': 'error',
                    'errors': {'email': u"Tietokannasta ei löytynyt jäsentä antamallasi osoitteella."}}

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
                       # This is safe, since at join there will be only one
                       # invoice anyway
                       "invoice": member.invoices.get(status=Invoice.STATUS.sent)}
            return render(request, "members/confirm_join_success.html", context)

    return render(request, "members/confirm_join_error.html")


def confirm_email_change(request, token):
    form = ConfirmationForm({'token': token})
    if form.is_valid():
        member = form.save()
        # See confirm_join - this may be buggy behavior
        if member:
            return render(request, "members/confirm_email_success.html",
                    {"member": member})

    return render(request, "members/confirm_email_error.html")


def edit(request, signed_id):
    signer = TimestampSigner()
    try:
        id = signer.unsign(signed_id, max_age=30 * 60)  # 30 minutes
        member = Member.objects.get(pk=id)
    except (BadSignature, SignatureExpired, Member.DoesNotExist):
        return render(request, "members/edit_failed.html")

    member_form = MemberForm(instance=member)
    email_form = MemberEmailEditForm(instance=member)

    if request.method == "POST":
        if "edit_member" in request.POST:
            member_form = MemberForm(request.POST, instance=member)
            if member_form.is_valid():
                member_form.save()
                messages.success(request, "Jäsentiedot tallennettu.")
                return HttpResponseRedirect(request.get_full_path())
            else:
                messages.error(request, "Korjaa jäsentiedoissa esiintyvät virheet.")
        elif "edit_email" in request.POST:
            email_form = MemberEmailEditForm(request.POST, instance=member)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, u"Syöttämääsi sähköpostiosoitteeseen %s lähetettiin vahvistusviesti, \
                        josta löytyvää linkkiä sinun tulee käydä klikkaamassa vahvistaaksesi muutoksen." % email_form.cleaned_data["email"])
                return HttpResponseRedirect(request.get_full_path())
            else:
                messages.error(request, "Korjaa virheet.")

    try:
        years_invoice = member.invoices.get(for_year=datetime.date.today().year)
    except Invoice.DoesNotExist:
        years_invoice = None

    return render(request, "members/edit.html", {"member": member,
                                                 "member_form": member_form,
                                                 "email_form": email_form,
                                                 "years_invoice": years_invoice})
