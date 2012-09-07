# encoding: utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from dotmembership.apps.members.models import Member


# Create your models here.
class Invoice(models.Model):
    STATUS_CHOICES = ((0, _(u"luotu")),
                    (1, _(u"lähetetty")),
                    (2, _(u"maksettu")),
                    (3, _(u"erääntynyt")),
                    (4, _(u"poistettu")))
    member = models.ForeignKey(Member, related_name="invoice")

    status = models.IntegerField(_(u"tila"), choices=STATUS_CHOICES)

    # Dates
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"luotu"))
    duedate = models.DateField(verbose_name=_(u"eräpäivä"))

    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u"summa"))
    # Automatically calculated at post_save based on the id

    reference_number = models.IntegerField(_(u"viitenumero"), blank=True, editable=False)


@receiver(post_save, sender=Invoice)
def calculate_reference_number(sender, instance, created, **kwargs):
    """
    Calculates reference number for
    """
    if created:
        # One-liner to calculate reference number :)
        instance.reference_number = instance.id + str(-sum(int(x)*[7,3,1][i%3] for i, x in enumerate(instance.reference_number[::-1])) % 10)
        instance.save()
