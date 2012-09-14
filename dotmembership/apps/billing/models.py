# encoding: utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

import reversion

from model_utils import Choices
from datetime import timedelta, date

from dotmembership.apps.members.models import Member


# Create your models here.
class Invoice(models.Model):
    STATUS = Choices(("created", _(u"luotu")),
                     ("sent", _(u"lähetetty")),
                     ("paid", _(u"maksettu")),
                     ("due", _(u"erääntynyt")),
                     ("missed", _(u"välistä")))

    PAYMENT = Choices(("cash", _(u"käteinen")), ("bank", _(u"pankki")))

    member = models.ForeignKey(Member, related_name="invoices")

    status = models.CharField(_(u"tila"), choices=STATUS, default=STATUS.created, max_length=15)

    # Year of the membership payment invoiced here
    for_year = models.IntegerField(_(u"kohdevuosi"))

    # Dates
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"luotu"))
    due_date = models.DateField(verbose_name=_(u"eräpäivä"), blank=True)
    payment_date = models.DateField(verbose_name=_(u"maksupäivä"), blank=True, null=True)

    payment_method = models.CharField(_(u"maksutapa"), choices=PAYMENT, max_length=15, blank=True, null=True)

    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u"summa"))
    # Automatically calculated at post_save based on the id

    reference_number = models.IntegerField(_(u"viitenumero"), blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=14)

        super(Invoice, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}, {1}".format(self.member, self.for_year)

reversion.register(Invoice)


@receiver(post_save, sender=Invoice)
def calculate_reference_number(sender, instance, created, **kwargs):
    """
    Calculates reference number for
    """
    if created:
        # One-liner to calculate reference number :)
        instance.reference_number = int(str(instance.id) + str(-sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(str(instance.id)[::-1])) % 10))
        instance.save()
