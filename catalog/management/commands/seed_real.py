"""Load 150 REAL products with real photos from the DummyJSON catalog API.

Usage:  python manage.py seed_real
Uses only the standard library (no new dependencies).
Prices are converted USD -> EGP. Photos are hotlinked from the DummyJSON CDN
and stored in Product.image_url (uploaded files in Product.image win).
"""
import json
import urllib.request
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

API = 'https://dummyjson.com/products?limit=150&select=title,description,price,stock,category,thumbnail,images'
USD_EGP = 48

CATEGORY_MAP = {
    'smartphones': 'Mobiles', 'tablets': 'Mobiles', 'mobile-accessories': 'Mobiles',
    'laptops': 'Laptops',
    'mens-shirts': 'Fashion', 'mens-shoes': 'Fashion', 'mens-watches': 'Fashion',
    'sunglasses': 'Fashion', 'tops': 'Fashion', 'womens-bags': 'Fashion',
    'womens-dresses': 'Fashion', 'womens-jewellery': 'Fashion',
    'womens-shoes': 'Fashion', 'womens-watches': 'Fashion',
    'furniture': 'Home', 'groceries': 'Home', 'home-decoration': 'Home',
    'kitchen-accessories': 'Home',
    'beauty': 'Beauty', 'fragrances': 'Beauty', 'skin-care': 'Beauty',
    'motorcycle': 'Sports', 'sports-accessories': 'Sports', 'vehicle': 'Sports',
}


class Command(BaseCommand):
    help = 'Load 150 real products with real photos (DummyJSON)'

    def handle(self, *args, **options):
        req = urllib.request.Request(API, headers={'User-Agent': 'E-Shop-Django/1.0'})
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.loads(res.read().decode('utf-8'))

        made, updated = 0, 0
        for item in data['products']:
            cat_name = CATEGORY_MAP.get(item['category'], item['category'].replace('-', ' ').title())
            category, _ = Category.objects.get_or_create(name=cat_name)
            photo = item.get('thumbnail') or (item.get('images') or [''])[0]
            defaults = {
                'category': category,
                'description': item['description'],
                'price': int(item['price'] * USD_EGP),
                'stock': max(0, int(item.get('stock', 0))),
                'image_url': photo,
                'is_active': True,
            }
            _, created = Product.objects.update_or_create(name=item['title'], defaults=defaults)
            made += created
            updated += not created

        self.stdout.write(self.style.SUCCESS(
            f'Loaded {len(data["products"])} real products ({made} new, {updated} updated).'))
