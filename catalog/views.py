from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):
    """Req 25 + 27-31: active products + search/filter/ordering + friendly empty message."""
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()

    q = request.GET.get('q', '').strip()
    cat = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    ordering = request.GET.get('ordering', '')

    if q:
        products = products.filter(name__icontains=q)
    if cat:
        products = products.filter(category__slug=cat)
    if min_price:
        try:
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass
    if ordering in ('price', '-price', 'name', '-name'):
        products = products.order_by(ordering)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
    })


def product_detail(request, slug):
    """Req 26: product details page (active only for customers)."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, 'catalog/product_detail.html', {'product': product, 'related': related})


def white_friday(request):
    """White Friday deals page: active products with a discount, biggest first."""
    deals = (Product.objects.filter(is_active=True, discount_percent__gt=0)
             .select_related('category').order_by('-discount_percent'))
    return render(request, 'catalog/white_friday.html',
                  {'deals': deals, 'biggest': deals.first()})
