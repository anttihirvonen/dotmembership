from django.contrib import admin
import reversion

from .models import Invoice


class InvoiceAdmin(reversion.VersionAdmin):
    readonly_fields = ("reference_number",)

admin.site.register(Invoice, InvoiceAdmin)
