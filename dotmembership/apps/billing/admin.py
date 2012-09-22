from django.contrib import admin
import reversion

from .models import Invoice


class InvoiceAdmin(reversion.VersionAdmin):
    readonly_fields = ("reference_number", "for_year")
    list_display = ("member", "status", "reference_number")
    list_filter = ("status",)
    actions = None

admin.site.register(Invoice, InvoiceAdmin)
