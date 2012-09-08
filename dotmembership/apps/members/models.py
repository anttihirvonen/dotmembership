# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


class Member(models.Model):
    MEMBERSHIP = Choices(("normal", _(u"normaali")),
                         ("support", _(u"kannatus")),
                         ("honorary", _(u"kunnia")))

    # The important data
    first_name = models.CharField(_(u"etunimi"), max_length=30)
    last_name = models.CharField(_(u"sukunimi"), max_length=30)
    email = models.EmailField(_(u"sähköpostiosoite"), help_text=_(u"Syötä toimiva sähköpostiosoite."))
    home_town = models.CharField(_(u"kotipaikka"), max_length=32)

    # Not-so-important data (nice to know..)
    # Free text for school, choices are shown on the front end with free text
    # input (same for major)
    school = models.CharField(_(u"koulu"), max_length=64, blank=True,
                              help_text=_(u"Mikäli olet käynyt/käyt useampia kouluja, merkitse tähän viimeisin."))
    major = models.CharField(_(u"pääaine"), max_length=64, blank=True,
                             help_text=_(u"Edellisessä mainitussa koulussa opiskelemasi pääaine."))
    class_year = models.IntegerField(_(u"Valmistumisvuosi"), blank=True, null=True,
                                     help_text=_(u"Vuosi, jolloin valmistuit/arvioit valmistuvasi."))

    # Membership data
    joined = models.DateTimeField(_(u"liittynyt"), auto_now_add=True, editable=False)
    membership_type = models.CharField(_(u"jäsentyyppi"), choices=MEMBERSHIP, max_length=15)

    def __unicode__(self):
        return "{0}, {1} ({2})".format(self.last_name, self.first_name, self.id)

    class Meta:
        verbose_name = _(u"jäsen")
        verbose_name_plural = _(u"jäsenet")
