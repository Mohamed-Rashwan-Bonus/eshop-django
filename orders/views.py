from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from cart.cart import Cart
from catalog.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    """Req 42-50: auth only, shipping form, server total, create order+items, reduce stock, clear cart."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, 'Your cart is empty.')
        return redirect('catalog:product_list')

    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            total = cart.total()  # req 45: calculated on server
            order = form.save(commit=False)
            order.user = request.user
            order.total = total
            order.save()
            for line in cart.items():
                p = line['product']
                if line['qty'] > p.stock:
                    messages.error(request, f'Only {p.stock} of {p.name} left.')
                    transaction.set_rollback(True)
                    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})
                OrderItem.objects.create(
                    order=order, product=p,
                    product_name=p.name, price=p.price, quantity=line['qty'],
                )
                Product.objects.filter(pk=p.pk).update(stock=F('stock') - line['qty'])  # req 48
            cart.clear()  # req 49
        return redirect('orders:confirmation', order_id=order.id)  # req 50
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def history(request):
    """Req 51."""
    return render(request, 'orders/history.html', {'orders': Order.objects.filter(user=request.user)})


@login_required
def detail(request, order_id):
    """Req 52,53,54: number, date, items, qty, prices, total — own orders only."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})
