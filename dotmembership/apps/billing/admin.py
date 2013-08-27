from django.contrib import admin
import reversion

from .models import Invoice, AnnualFee


class InvoiceAdmin(reversion.VersionAdmin):
    readonly_fields = ('amount', "reference_number", "for_year", 'member', 'created', 'fee', 'due_date')
    fields = ('member', 'created', 'fee', 'due_date', 'amount', 'reference_number', 'status', 'payment_date',
            'payment_method')
    list_display = ("member", "status", "reference_number")
    list_filter = ("status",)
    actions = None

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(AnnualFee)
