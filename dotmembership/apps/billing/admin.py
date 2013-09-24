from django.contrib import admin
import reversion

from .models import Invoice, AnnualFee


class AnnualFeeAdmin(reversion.VersionAdmin):
    list_display = ('year', 'amount', 'start_date', 'end_date')


class InvoiceAdmin(reversion.VersionAdmin):
    readonly_fields = ('amount', "reference_number", "for_year", 'member', 'created', 'fee', 'due_date')
    fields = ('member', 'created', 'fee', 'due_date', 'amount', 'reference_number', 'status', 'payment_date',
            'payment_method')
    list_display = ("member", "status", "reference_number", "fee")
    list_filter = ("status", "fee")
    actions = None

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(AnnualFee, AnnualFeeAdmin)
