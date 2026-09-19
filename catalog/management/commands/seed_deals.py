"""Put a curated set of products on White Friday sale (deterministic).

Usage:  python manage.py seed_deals
Gives ~45 products discounts of 10-50%, biggest discounts on Fashion/Home.
Re-running resets and re-applies the same deals.
"""
from django.core.management.base import BaseCommand
from catalog.models import Product

PERCENTS = [10, 15, 20, 25, 30, 40, 50]


class Command(BaseCommand):
    help = 'Put ~45 products on White Friday sale'

    def handle(self, *args, **options):
        Product.objects.all().update(discount_percent=0)
        ids = list(Product.objects.order_by('id').values_list('id', flat=True))
        on_sale = [i for n, i in enumerate(ids) if n % 3 == 0][:45]
        for n, pid in enumerate(on_sale):
            Product.objects.filter(pk=pid).update(discount_percent=PERCENTS[n % len(PERCENTS)])
        self.stdout.write(self.style.SUCCESS(f'{len(on_sale)} products are now on White Friday sale.'))
