from django.contrib import admin
import reversion

from .models import Member


class MemberAdmin(reversion.VersionAdmin):
    list_display = ("full_name", "email", "last_payment_year", "last_payment_status")

    def last_payment_year(self, member):
        return member.invoices.latest("for_year").for_year

    def last_payment_status(self, member):
        return member.invoices.latest("for_year").status


admin.site.register(Member, MemberAdmin)
