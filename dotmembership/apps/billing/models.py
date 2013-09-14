# encoding: utf-8
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.db.models.query import QuerySet
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from mailer import send_mail as mailer_send_mail

import reversion

from model_utils import Choices
from model_utils.managers import PassThroughManager
from datetime import timedelta, date, datetime

from dotmembership.apps.members.models import Member


class AnnualFeeManager(models.Manager):
    def get_fee_for_date(self, date):
        fee = self.get(start_date__lte=date, end_date__gte=date)
        return fee

    def get_active_fee(self):
        return self.get_fee_for_date(date.today())


class AnnualFee(models.Model):
    """
    Annual fee for membership.

    When a new member registers, the current annual fee
    (determined by current date, start_date and end_date) is
    used to create an invoice for the membership. Note that if
    annual fee for current date can't be found, an exception is raised.
    It's therefore admin's responsibility to ensure that a fee
    exists for any date during which a new user might register.
    Fees also should not overlap (too lazy to code any checks
    for validity...)

    When a new annual fee becomes active the billing cycle should be run,
    which generates new invoices for all existing members.
    TODO: when implemented, doc here the command name
    """
    year = models.IntegerField(_(u'vuosi'), unique=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u"summa"))
    start_date = models.DateField(_(u'kauden alkamispäivä'))
    end_date = models.DateField(_(u'kauden loppumispäivä'))

    objects = AnnualFeeManager()

    def __unicode__(self):
        return u'{0}'.format(self.year)

reversion.register(AnnualFee)


class InvoiceQuerySet(QuerySet):
    def unpaid(self):
        """
        Returns unpaid invoices.
        """
        from .models import Invoice
        return self.exclude(status=Invoice.STATUS.paid).exclude(status=Invoice.STATUS.missed)


class Invoice(models.Model):
    STATUS = Choices(("created", _(u"luotu")),   # created, not shown/sent to member
                     ("sent", _(u"lähetetty (maksamatta)")),  # member has receiver invoice
                     ("paid", _(u"maksettu")),   # member has paid the invoide
                     ("due", _(u"erääntynyt")),  # the invoice wasn't paid before due date
                     ("missed", _(u"välistä (jätetty maksamatta)")))  # the invoice wasn't paid during year

    PAYMENT = Choices(("cash", _(u"käteinen")), ("bank", _(u"pankki")))

    member = models.ForeignKey(Member, related_name="invoices")

    status = models.CharField(_(u"tila"), choices=STATUS, default=STATUS.created, max_length=15)

    # fee that's invoiced
    fee = models.ForeignKey(AnnualFee, null=True, default=None)

    # Dates
    created = models.DateTimeField(default=timezone.now, verbose_name=_(u"luotu"))
    due_date = models.DateField(verbose_name=_(u"eräpäivä"), blank=True)
    payment_date = models.DateField(verbose_name=_(u"maksupäivä"), blank=True, null=True)

    payment_method = models.CharField(_(u"maksutapa"), choices=PAYMENT, max_length=15, blank=True, null=True)

    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u"summa"))
    # Automatically calculated at post_save based on the id

    reference_number = models.IntegerField(_(u"viitenumero"), blank=True, null=True)

    objects = PassThroughManager.for_queryset_class(InvoiceQuerySet)()

    @property
    def paid(self):
        return self.status == self.STATUS.paid

    @property
    def for_year(self):
        return self.fee.year

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.status == self.STATUS.paid and not (self.payment_date and self.payment_method):
            raise ValidationError(_(u"Syötä maksupäivä ja -tapa."))

    def send_payment_mail(self):
        subject = _(u"DOTin jäsenmaksutiedot vuodelle {0}".format(self.for_year))
        body = render_to_string("billing/mails/new_invoice.txt",
                {'invoice': self})

        # use mailer to send mail
        mailer_send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.member.email])

    def save(self, *args, **kwargs):
        # calculate due date
        if not self.due_date:
            self.due_date = self.created + timedelta(days=14)

        # amount from fee object
        if not self.amount:
            self.amount = self.fee.amount

        send_paid_mail = False
        if self.status == self.STATUS.paid:
            previous = Invoice.objects.get(pk=self.pk)
            if previous.status != self.STATUS.paid:
                # status has changed – send email after save
                send_paid_mail = True

        super(Invoice, self).save(*args, **kwargs)

        if send_paid_mail:
            subject = _(u"Jäsenmaksusi on kirjattu maksetuksi")
            body = render_to_string("billing/mails/invoice_paid.txt",
                                    {'invoice': self})
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.member.email])

    def __unicode__(self):
        return u"{0}, {1}".format(self.member, self.for_year)

    class Meta:
        unique_together = ("member", "fee")
        get_latest_by = "created"

reversion.register(Invoice)


def generate_invoices_for_fee(fee, dry_run=False):
    """
    Uses given fee to generate invoices for all members.
    Also sends mails about the new invoices.

    If an invoice for the given fee already exists, does nothing.
    """
    for member in Member.objects.all():
        try:
            invoice = Invoice.objects.get(member=member, amount=fee.amount, fee=fee)
        except Invoice.DoesNotExist:
            # Skip rest of the function if runnin' dry
            if dry_run:
                print u"Would generate invoice for member {0}, {1}".format(member.id, member.email)
                continue

            print u"Generating invoice for member {0}, {1}".format(member.id, member.email)
            invoice = Invoice.objects.create(member=member, amount=fee.amount, fee=fee)
            invoice.send_payment_mail()
            invoice.status = Invoice.STATUS.sent
            invoice.save()


def archive_old_unpaid_invoices(fee, dry_run=False):
    """
    TODO: document / test
    """
    # go through invoices that have not been paid
    # TODO: move the long query to InvoiceManager as a method
    for invoice in Invoice.objects.exclude(fee=fee).exclude(status=Invoice.STATUS.paid).exclude(status=Invoice.STATUS.missed):
        print u'Archivable Invoice found: status={0} fee={1} member={2}'.format(invoice.status, invoice.fee, invoice.member)
        invoice.status = Invoice.STATUS.missed
        if not dry_run:
            invoice.save()


@receiver(post_save, sender=Invoice)
def calculate_reference_number(sender, instance, created, **kwargs):
    """
    Calculates reference number for the invoice.
    """
    # TODO: this should be moved to save() as the instance is modified
    if created:
        # One-liner to calculate reference number :)
        instance.reference_number = int(str(instance.id) + str(-sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(str(instance.id)[::-1])) % 10))
        instance.save()
