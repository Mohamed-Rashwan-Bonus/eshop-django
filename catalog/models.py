from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Req 10-14: each product belongs to one category."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Req 15-24: name, description, price, stock, image, category, active status."""
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,  # req 12: can't delete category with products
        related_name='products',
    )
    name = models.CharField(max_length=200)  # title
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Remote photo URL (used when no file is uploaded).')
    discount_percent = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='White Friday deal: 0 = no discount, e.g. 25 = 25% off.',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, i = base, 2
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{i}'
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # --- display helpers for badges ---
    @property
    def is_new(self):
        return self.created_at >= timezone.now() - timedelta(days=14)

    @property
    def is_low_stock(self):
        return 0 < self.stock <= 5

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    @property
    def has_deal(self):
        return self.is_active and self.discount_percent > 0

    @property
    def current_price(self):
        """Price the customer actually pays (deal-aware)."""
        if self.discount_percent:
            return round(self.price * (100 - self.discount_percent) / 100, 2)
        return self.price

    def cover_url(self):
        """Uploaded photo first, then the real remote photo, then a demo placeholder."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return f'https://picsum.photos/seed/{self.slug or self.pk or "shop"}/800/600'
