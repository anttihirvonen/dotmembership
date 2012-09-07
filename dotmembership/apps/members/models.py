# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

# Create your models here.
class Member(models.Model):
    MEMBERSHIP = Choices(("normal", _(u"normaali")),
                         ("support", _(u"kannatus")),
                         ("honorary", _(u"kunnia")))

    first_name = models.CharField(_(u"etunimi"), max_length=30)
    last_name = models.CharField(_(u"sukunimi"), max_length=30)
    email = models.EmailField(_(u"sähköpostiosoite"))

    joined = models.DateTimeField(_(u"liittynyt"), auto_now_add=True, editable=False)
    membership_type = models.CharField(_(u"jäsentyyppi"), choices=MEMBERSHIP, max_length=15)

    def __unicode__(self):
        return "{0}, {1} ({2})".format(self.last_name, self.first_name, self.id)

    class Meta:
        verbose_name = _(u"jäsen")
        verbose_name_plural = _(u"jäsenet")
