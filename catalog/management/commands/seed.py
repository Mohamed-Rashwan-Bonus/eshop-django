from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Create demo categories + products for the team presentation'

    def handle(self, *args, **options):
        cats = {
            'Mobiles': 'Smartphones and accessories',
            'Laptops': 'Laptops and computers',
            'Fashion': 'Clothes, shoes and watches',
            'Home': 'Home and kitchen essentials',
        }
        for name, desc in cats.items():
            Category.objects.get_or_create(name=name, defaults={'description': desc})

        demo = [
            ('iPhone 15', 'Mobiles', 60000, 10, 'Latest Apple smartphone with a superb camera and all-day battery.'),
            ('Samsung Galaxy A55', 'Mobiles', 18500, 20, 'Mid-range Samsung with a big battery and smooth 120Hz display.'),
            ('Xiaomi Redmi Note 13', 'Mobiles', 9500, 3, 'Budget champion with a great screen and fast charging.'),
            ('HP Pavilion 15', 'Laptops', 35000, 7, 'Everyday laptop for study and work with SSD storage.'),
            ('Lenovo IdeaPad Slim', 'Laptops', 28000, 12, 'Lightweight laptop with long battery life for students.'),
            ('Nike Running Shoes', 'Fashion', 4200, 15, 'Comfortable cushioned running shoes for daily training.'),
            ('Classic Leather Watch', 'Fashion', 6500, 4, 'Elegant leather-strap watch that fits any occasion.'),
            ('Cotton Hoodie', 'Fashion', 1200, 25, 'Soft heavyweight cotton hoodie, perfect for winter.'),
            ('Air Fryer XL', 'Home', 7500, 8, 'Oil-free healthy cooking with 5.5L family capacity.'),
            ('Ceramic Cookware Set', 'Home', 5200, 0, 'Non-stick ceramic pots set. Currently out of stock.'),
        ]
        for name, cat, price, stock, desc in demo:
            Product.objects.get_or_create(
                name=name,
                defaults={'category': Category.objects.get(name=cat), 'price': price,
                          'stock': stock, 'description': desc, 'is_active': True},
            )
        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
