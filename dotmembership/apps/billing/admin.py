from django.contrib import admin
import reversion

from .models import Invoice


class InvoiceAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Invoice, InvoiceAdmin)
