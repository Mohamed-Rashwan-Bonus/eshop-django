from django.db import models
from django.conf import settings
from catalog.models import Product
from accounts.models import validate_egyptian_phone


class Order(models.Model):
    """Req 46: created on checkout with server-calculated total."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=16, validators=[validate_egyptian_phone])
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} - {self.user.email}'


class OrderItem(models.Model):
    """Req 47."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at purchase time
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.price * self.quantity
