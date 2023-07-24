from django.core.management import BaseCommand
from store_api.models import Product
from datetime import datetime, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo agg')
        product = Product.objects.filter(sale__isnull=False, sale__date_to__gte=datetime.now() + timedelta(hours=3))
        print(product)
        self.stdout.write('Done')
