
from django.core.management.base import BaseCommand
from dotmembership.apps.billing.models import AnnualFee, Invoice


class Command(BaseCommand):
    help = "Dumps out email addresses for members who haven't paid current annual "\
           "membership fee."

    def handle(self, *args, **options):
        fee = AnnualFee.objects.get_active_fee()
        # Include only members with unpaid current invoice.
        # Note that this doesn't filter out members who didn't
        # pay the free last year (currently invoices are generated
        # for all members, even those who have missed payments).
        # Not a problem for now, but should be probably changed later on.
        invoices = Invoice.objects.filter(fee=fee,
                                          status__in=[Invoice.STATUS.sent,
                                                      Invoice.STATUS.due])
        for invoice in invoices:
            print(u"{0},".format(invoice.member.email)),
