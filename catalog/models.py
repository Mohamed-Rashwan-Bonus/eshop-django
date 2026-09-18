from datetime import timedelta
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
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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

    def cover_url(self):
        """Uploaded image if present, else a deterministic demo photo."""
        if self.image:
            return self.image.url
        return f'https://picsum.photos/seed/{self.slug or self.pk or "shop"}/800/600'
