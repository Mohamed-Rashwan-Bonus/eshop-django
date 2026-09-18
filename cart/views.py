from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    qty = int(request.POST.get('qty', 1)) if request.method == 'POST' else 1
    cart = Cart(request)
    if not cart.add(product, qty):
        messages.error(request, f'Only {product.stock} in stock.')
    else:
        messages.success(request, f'{product.name} added to cart.')
    return redirect('cart:detail')


def cart_increase(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    if not cart.increase(product):
        messages.error(request, f'Only {product.stock} in stock.')
    return redirect('cart:detail')


def cart_decrease(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).decrease(product)
    return redirect('cart:detail')


def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove(product)
    return redirect('cart:detail')


def cart_clear(request):
    Cart(request).clear()
    return redirect('cart:detail')
