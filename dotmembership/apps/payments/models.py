from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.members.models import Member


# Create your models here.
class Invoice(models.Model):
    STATUS_CHOICES = ((0, "luotu"),
                    (1, "lähetetty"),
                    (2, "maksettu"),
                    (3, "erääntynyt"),
                    (4, "poistettu"))
    member = models.ForeignKey(Member, related_name="invoice")

    status = models.IntegerField("tila", choices=STATUS_CHOICES)

    # Dates
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'luotu')
    duedate = models.DateField(verbose_name=u'eräpäivä')

    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=u'summa')
    # Automatically calculated at post_save based on the id

    reference_number = models.IntegerField("viitenumero", blank=True, editable=False)


@receiver(post_save, sender=Invoice)
def calculate_reference_number(sender, instance, created, **kwargs):
    """
    Calculates reference number for
    """
    if created:
        # One-liner to calculate reference number :)
        instance.reference_number = instance.id + str(-sum(int(x)*[7,3,1][i%3] for i, x in enumerate(instance.reference_number[::-1])) % 10)
        instance.save()
