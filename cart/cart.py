from catalog.models import Product


class Cart:
    """Req 41: cart stored in Django session as {product_id: qty}."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, qty=1):
        """Req 32,33,40: add with quantity, never exceed stock."""
        pid = str(product.id)
        current = self.cart.get(pid, 0)
        new_qty = current + int(qty)
        if new_qty > product.stock:
            return False  # req 40
        self.cart[pid] = new_qty
        self.save()
        return True

    def set_qty(self, product, qty):
        if qty <= 0:
            return self.remove(product)
        if qty > product.stock:
            return False
        self.cart[str(product.id)] = qty
        self.save()
        return True

    def increase(self, product):
        return self.add(product, 1)

    def decrease(self, product):
        pid = str(product.id)
        if pid in self.cart:
            self.cart[pid] -= 1
            if self.cart[pid] <= 0:
                del self.cart[pid]
            self.save()

    def remove(self, product):
        self.cart.pop(str(product.id), None)
        self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        self.cart = self.session['cart']

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())

    def items(self):
        """Yield {product, qty, subtotal} + skip deleted products. Req 38."""
        products = Product.objects.filter(id__in=self.cart.keys())
        for p in products:
            qty = self.cart[str(p.id)]
            yield {'product': p, 'qty': qty, 'subtotal': p.price * qty}

    def total(self):
        """Req 39."""
        return sum(i['subtotal'] for i in self.items())
