# encoding: utf-8
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.db.models.query import QuerySet
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

import reversion

from model_utils import Choices
from model_utils.managers import PassThroughManager
from datetime import timedelta, date

from dotmembership.apps.members.models import Member


class AnnualFee(models.Model):
    """
    Annual fee for membership.

    When a new member registers, the current annual fee
    (determined by current date, start_date and end_date) is
    used to create an invoice for the membership. Note that if
    annual fee for current date can't be found, an exception is raised.
    It's therefore admin's responsibility to ensure that a fee
    exists for any date during which a new user might register.

    When a new annual fee becomes active the billing cycle should be run.
    It generates invoices for all existing users based on the
    selected fee and sends new invoices to members via email.
    """
    year = models.IntegerField(_(u'vuosi'), unique=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u"summa"))
    start_date = models.DateField(_(u'kauden alkamispäivä'))
    end_date = models.DateField(_(u'kauden loppumispäivä'))


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
                     ("missed", _(u"välistä")))  # the invoice wasn't paid during year

    PAYMENT = Choices(("cash", _(u"käteinen")), ("bank", _(u"pankki")))

    member = models.ForeignKey(Member, related_name="invoices")

    status = models.CharField(_(u"tila"), choices=STATUS, default=STATUS.created, max_length=15)

    # Year of the membership payment invoiced here
    for_year = models.IntegerField(_(u"kohdevuosi"), editable=False)

    # Dates
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"luotu"))
    due_date = models.DateField(verbose_name=_(u"eräpäivä"), blank=True)
    payment_date = models.DateField(verbose_name=_(u"maksupäivä"), blank=True, null=True)

    payment_method = models.CharField(_(u"maksutapa"), choices=PAYMENT, max_length=15, blank=True, null=True)

    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u"summa"))
    # Automatically calculated at post_save based on the id

    reference_number = models.IntegerField(_(u"viitenumero"), blank=True, null=True, editable=False)

    objects = PassThroughManager.for_queryset_class(InvoiceQuerySet)()

    @property
    def paid(self):
        return self.status == self.STATUS.paid

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.status == self.STATUS.paid and not (self.payment_date and self.payment_method):
            raise ValidationError(_(u"Syötä maksupäivä ja -tapa."))

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=14)

        send_paid_mail = False
        if self.status == self.STATUS.paid:
            previous = Invoice.objects.get(pk=self.pk)
            if previous.status != self.STATUS.paid:
                # status has changed – send email
                send_paid_mail = True

        super(Invoice, self).save(*args, **kwargs)

        if send_paid_mail:
            subject = _(u"Jäsenmaksusi vuodelle {0} kirjattu".format(self.for_year))
            body = render_to_string("billing/mails/invoice_paid.txt",
                                    {'invoice': self})
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.member.email])

    def __unicode__(self):
        return u"{0}, {1}".format(self.member, self.for_year)

    class Meta:
        unique_together = ("member", "for_year")
        get_latest_by = "for_year"

reversion.register(Invoice)


@receiver(post_save, sender=Invoice)
def calculate_reference_number(sender, instance, created, **kwargs):
    """
    Calculates reference number for
    #TODO: this should be probably moved to save(), as it modifies
    the instance
    """
    if created:
        # One-liner to calculate reference number :)
        instance.reference_number = int(str(instance.id) + str(-sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(str(instance.id)[::-1])) % 10))
        instance.save()
