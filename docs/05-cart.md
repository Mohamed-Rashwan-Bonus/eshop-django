# عضو 5 — سلة المشتريات (Cart) — الشروط 32 ل 41

## 1. مهمتك ايه بالظبط
السلة كاملة: إضافة + كمية + زيادة/نقصان + مسح عنصر + تفريغ + المجاميع — وكل ده من غير جدول داتابيز. ملفاتك: `cart/cart.py` (الكلاس) و `cart/views.py` و `cart/urls.py`.

## 2. المفاهيم اللي لازم تعرف تشرحها
- الـ session يعني مخزن مؤقت لكل زائر على السيرفر (مرتبط بـ cookie) — مناسب للسلة عشان الزائر المجهول ملوش صف في الداتابيز.
- السلة عندنا قاموس بسيط: رقم المنتج هو المفتاح والكمية هي القيمة، مثلا `{'7': 2}`.
- `session.modified = True` إجبارية عشان Django يحفظ التعديل على القاموس.
- حارس المخزون: أي كمية بتتطلب بتتقارن بـ stock قبل الحفظ (شرط 40).

## 3. الملفات بتاعتك سطر بسطر
### cart/cart.py — قلب السلة
```
def __init__(self, request):
    self.session = request.session
    cart = self.session.get('cart')
    if cart is None:
        cart = self.session['cart'] = {}
    self.cart = cart
```
```
def add(self, product, qty=1):          # شرط 32 و33
    new_qty = self.cart.get(pid, 0) + int(qty)
    if new_qty > product.stock:
        return False                    # شرط 40: مستحيل تتجاوز المخزون
    self.cart[pid] = new_qty
    self.save()
    return True
```
```
def items(self):                        # شرط 38
    products = Product.objects.filter(id__in=self.cart.keys())
    for p in products:
        yield {'product': p, 'qty': qty, 'subtotal': p.current_price * qty}
def total(self):                        # شرط 39
    return sum(i['subtotal'] for i in self.items())
def savings(self):
    return sum((price - current_price) * qty ...)   # توفير الوايت فرايداي
```
- شرط 41: مفيش موديل للسلة — كلها session.
- لو منتج اتمسح من الداتابيز، الـ filter مش هيجيبه فبيختفي من السلة لوحده بأمان.
- الـ subtotal بيستخدم current_price يعني سعر الخصم لو موجود.

### cart/views.py — الحركات
- add/increase/decrease/remove/clear كل واحدة view صغيرة بتنده الكلاس وترجع للتفاصيل.
- لو الكمية فوق المخزون بيظهر messages.error بعدد المتاح بدل ما يضرب.

## 4. انت مربوط بمين
- عضو 3: بتقرا منه stock و current_price لحظيا (فلو الأدمن غير سعر، السلة تتحسب بالجديد).
- عضو 4: زرار Add اللي في كروته بينده add بتاعتك.
- عضو 6: بيستلم منك السلة في الـ checkout ويصفرها بعد الأوردر.

## 5. أسئلة مناقشة متوقعة
- س: ليه session مش داتابيز؟ ج: الزائر المجهول ملوش حساب نخزن عليه، والـ session أسرع وأبسط، والتحويل لأوردر بيحصل عند الدفع.
- س: لو طلب كمية أكبر من المخزون؟ ج: add بترجع False والـ view بتطلع رسالة بعدد المتاح — واتجربت آليا.
- س: السلة بتفضل بعد قفل المتصفح؟ ج: طول ما الـ session cookie موجودة (default أسبوعين).
- س: الخصم بيتحسب فين؟ ج: الـ subtotal بيستخدم current_price، فأي خصم جديد بينعكس فورا حتى على سلة قديمة.

## 6. العرض اللايف بتاعك (دقيقتين)
1. ضيف منتج بكمية 2، زود ونقص من الأزرار.
2. حاول تطلب كمية أكبر من المخزون وورّي رسالة المنع.
3. ضيف منتج عليه خصم وورّي سطر You save في الملخص.
