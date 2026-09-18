from django.shortcuts import render
from catalog.models import Product, Category


def home(request):
    """Landing page: shows categories + latest active products."""
    categories = Category.objects.all()[:6]
    latest = Product.objects.filter(is_active=True).select_related('category').order_by('-created_at')[:8]
    return render(request, 'home.html', {'categories': categories, 'latest': latest})
