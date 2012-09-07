# encoding: utf-8
from django.db import models


# Create your models here.
class Member(models.Model):
    MEMBERSHIP_CHOICES = ((0, "normaali"),
                          (1, "kannatus")
                          (2, "kunnia"))
    first_name = models.CharField("etunimi", max_length=30)
    last_name = models.CharField("sukunimi", max_length=30)
    email = models.EmailField("sähköpostiosoite")

    membership_type = models.IntegerField("jäsentyyppi", choices=MEMBERSHIP_CHOICES)

    class Meta:
        verbose_name = u"jäsen"
        verbose_name_plural = u"jäsenet"
