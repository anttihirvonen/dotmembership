# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings

from model_utils import Choices


class Member(models.Model):
    MEMBERSHIP = Choices(("normal", _(u"varsinainen")),
                         ("support", _(u"kannatus")),
                         ("honorary", _(u"kunnia")))

    PUBLIC_FIELDS = ("id", "first_name", "last_name", "email", "home_town",
                     "school", "major", "class_year", "joined")

    id = models.AutoField(_(u"jäsennumero"), primary_key=True)

    # The important data
    first_name = models.CharField(_(u"etunimi"), max_length=30)
    last_name = models.CharField(_(u"sukunimi"), max_length=30)
    email = models.EmailField(_(u"sähköpostiosoite"), help_text=_(u"Syötä toimiva sähköpostiosoite."), unique=True)
    home_town = models.CharField(_(u"kotipaikka"), max_length=32)

    # Not-so-important data (nice to know..)
    # Free text for school, choices are shown on the front end with free text
    # input (same for major)
    school = models.CharField(_(u"koulu"), max_length=64, blank=True,
                              help_text=_(u"Mikäli olet käynyt/käyt useampia kouluja, merkitse tähän viimeisin."))
    major = models.CharField(_(u"pääaine"), max_length=64, blank=True,
                             help_text=_(u"Edellisessä mainitussa koulussa opiskelemasi pääaine."))
    class_year = models.IntegerField(_(u"valmistumisvuosi"), blank=True, null=True,
                                     help_text=_(u"Vuosi, jolloin valmistuit/arvioit valmistuvasi."))

    # Membership data
    joined = models.DateTimeField(_(u"liittymisaika"), auto_now_add=True, editable=False)
    membership_type = models.CharField(_(u"jäsentyyppi"), choices=MEMBERSHIP, max_length=15)

    @property
    def timestamped_id(self):
        """
        Returns self.id signed using TimestampSigner.
        """
        signer = TimestampSigner()
        return signer.sign(str(self.id))

    @property
    def edit_link(self):
        """
        Generates a link for member edit form.
        """
        return reverse("members-edit_member", args=[self.timestamped_id])

    def send_data_and_edit_link(self):
        subject = _(u"Jäsentietosi sekä muokkauslinkki")
        fields = self.PUBLIC_FIELDS
        # TODO: add invoicing details
        body = render_to_string("members/mails/data_and_edit_link.txt",
                                {'member': self,
                                 'base_url': "http://{0}".format(Site.objects.get_current().domain),
                                 'fields': fields})
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.email])

    def __unicode__(self):
        return u"{0}, {1} ({2})".format(self.last_name, self.first_name, self.id)

    class Meta:
        verbose_name = _(u"jäsen")
        verbose_name_plural = _(u"jäsenet")


@receiver(post_save, sender=Member, dispatch_uid="member.create_invoice_send_welcome_mail")
def create_first_invoice_and_send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # TODO: fast hack, refactor this later...
        import datetime
        from dotmembership.apps.billing.models import Invoice
        from django.conf import settings

        # TODO: don't hardcode amount
        invoice = instance.invoices.create(status=Invoice.STATUS.sent,
                                           for_year=datetime.date.today().year,
                                           amount="5")
        subject = _(u"Tervetuloa DOTin jäseneksi!")
        fields = Member.PUBLIC_FIELDS
        body = render_to_string("members/mails/welcome.txt",
                                {'member': instance,
                                 'fields': fields,
                                 'invoice': invoice})
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [instance.email])
