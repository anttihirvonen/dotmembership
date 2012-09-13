# encoding: utf-8
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings
from django import forms

from generic_confirmation.forms import DeferredForm

from .models import Member


class MemberForm(DeferredForm):
    """
    The main form for registering a new member.
    """
    class Meta:
        model = Member
        fields = ("first_name", "last_name", "email", "home_town",
                  "school", "major", "class_year")

    def send_notification(self, user=None, instance=None):
        subject = _(u"Vahvista liittymisesi DOTin jäseneksi")
        body = render_to_string("members/mails/confirm_join.txt",
                                 {'token': instance.token,
                                  'base_url': "http://{0}".format(Site.objects.get_current().domain),
                                  'first_name': self.cleaned_data['first_name']})
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.cleaned_data['email']])


class MemberEmailForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("email",)
