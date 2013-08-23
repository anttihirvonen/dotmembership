from django.contrib import admin
import reversion

from .models import Member

# Global action disable, should be somwhere else..
admin.site.disable_action('delete_selected')

class MemberAdmin(reversion.VersionAdmin):
    list_display = ("full_name", "email", "last_invoice_year", "last_invoice_status")

    def last_invoice_year(self, member):
        return member.invoices.latest("fee").for_year

    def last_invoice_status(self, member):
        return member.invoices.latest("fee").status


admin.site.register(Member, MemberAdmin)
