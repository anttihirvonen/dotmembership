# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class Member(models.Model):
    MEMBERSHIP_CHOICES = ((0, _(u"normaali")),
                          (1, _(u"kannatus")),
                          (2, _(u"kunnia")))
    first_name = models.CharField(_(u"etunimi"), max_length=30)
    last_name = models.CharField(_(u"sukunimi"), max_length=30)
    email = models.EmailField(_(u"sähköpostiosoite"))

    membership_type = models.IntegerField(_(u"jäsentyyppi"), choices=MEMBERSHIP_CHOICES)

    class Meta:
        verbose_name = _(u"jäsen")
        verbose_name_plural = _(u"jäsenet")
