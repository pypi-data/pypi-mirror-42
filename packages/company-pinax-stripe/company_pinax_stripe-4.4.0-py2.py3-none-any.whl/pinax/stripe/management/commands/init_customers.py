from certsafe.apps.core.models import Company
from django.core.management.base import BaseCommand

from ...actions import customers


class Command(BaseCommand):

    help = "Create customer objects for existing users that do not have one"

    def handle(self, *args, **options):
        for company in Company.objects.filter(customer__isnull=True):
            customers.create(company=company, charge_immediately=False)
            self.stdout.write("Created customer for {0}\n".format(company.name))
