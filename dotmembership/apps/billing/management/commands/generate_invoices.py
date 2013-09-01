from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from dotmembership.apps.billing.models import generate_invoices_for_fee, AnnualFee, archive_old_unpaid_invoices


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
       make_option('--dry-run',
           action='store_true',
           dest='dry_run',
           default=False),
       make_option('--year',
           action='store',
           dest='year',
           type='int'),
       )
    help = 'Generates invoices'

    def handle(self, *args, **options):
        fee = AnnualFee.objects.get(year=options['year'])
        archive_old_unpaid_invoices(fee, options['dry_run'])
        generate_invoices_for_fee(fee, options['dry_run'])
