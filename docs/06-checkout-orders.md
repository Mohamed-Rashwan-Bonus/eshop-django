# عضو 6 — الدفع والأوردرات (Checkout + Orders) — الشروط 42 ل 54

## 1. مهمتك ايه بالظبط
أخطر جزء: تحويل السلة لأوردر حقيقي + تقليل المخزون + تاريخ الأوردرات. ملفاتك: `orders/models.py` و `orders/views.py` و `orders/forms.py`.

## 2. المفاهيم اللي لازم تعرف تشرحها
- الـ transaction.atomic يعني يا كل العمليات تنجح يا كلها تتلغي — مينفعش أوردر يتعمل من غير ما المخزون ينقص.
- `F('stock') - qty` يعني الخصم بيحصل جوه الداتابيز نفسها (آمن ضد طلبين في نفس الثانية).
- حساب المجموع على السيرفر (شرط 45) يعني منثقش في أي رقم جاي من المتصفح.
- سعر لحظة الشراء بيتخزن في OrderItem عشان لو السعر اتغير بعدين، الفاتورة القديمة تفضل صح.

## 3. الملفات بتاعتك سطر بسطر
### orders/models.py
```
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER, on_delete=models.CASCADE, related_name='orders')
    full_name, email, phone, address, city   # بيانات الشحن (شرط 43)
    total = models.DecimalField(...)         # محسوب على السيرفر (شرط 45)
    created_at = models.DateTimeField(auto_now_add=True)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name, price, quantity
    def subtotal(self): return self.price * self.quantity
```
- SET_NULL عشان لو منتج اتمسح بعد البيع، الأوردر يفضل موجود باسمه وسعره.

### orders/views.py — checkout (الشروط 42 ل 50)
```
@login_required                                    # شرط 42
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0: ... redirect ...           # سلة فاضية ملهاش checkout
    form = CheckoutForm(request.POST or None)     # بيانات الشحن + مراجعة السلة (43 و44)
    if POST and form.is_valid():
        with transaction.atomic():
            total = cart.total()                   # شرط 45: من السيرفر
            order = form.save(commit=False); order.user = request.user; order.total = total
            order.save()                           # شرط 46
            for line in cart.items():
                if line['qty'] > p.stock: rollback + رسالة
                OrderItem.objects.create(...)      # شرط 47 بسعر الخصم
                Product.objects.filter(pk=p.pk).update(stock=F('stock') - qty)  # شرط 48
            cart.clear()                           # شرط 49
        return redirect('orders:confirmation', ...)  # شرط 50
```

### history و detail (الشروط 51 ل 54)
```
Order.objects.filter(user=request.user)                       # شرط 51: أوردراتي بس
get_object_or_404(Order, id=order_id, user=request.user)      # شرط 54: أوردر غيري = 404
```
- شرط 53: صفحة التفاصيل فيها الرقم والتاريخ والأصناف والكميات والأسعار والمجموع.

## 4. انت مربوط بمين
- عضو 2: `request.user` هو صاحب الأوردر.
- عضو 5: بتستلم السلة وتصفرها، وبتستخدم نفس current_price.
- عضو 3: بتنقص الـ stock بتاعه.

## 5. أسئلة مناقشة متوقعة
- س: لو اتنين اشتروا آخر قطعة مع بعض؟ ج: الـ transaction + الـ F() بيخلوا واحد ينجح والتاني يشوف رسالة ان المخزون خلص.
- س: ليه المجموع من السيرفر؟ ج: عشان أي حد يقدر يعدل HTML المتصفح ويبعت total مزيف — احنا منحسبش غير من الداتابيز.
- س: لو منتج اتمسح بعد ما اتباع؟ ج: الأوردر محفوظ باسمه وسعره (SET_NULL) فالفاتورة سليمة.
- س: إزاي منعت حد يشوف أوردر حد؟ ج: كل استعلام فيه user=request.user، واتجربت: يوزر تاني بياخد 404.

## 6. العرض اللايف بتاعك (دقيقتين)
1. اعمل checkout كامل وورّي صفحة التأكيد.
2. افتح تاريخ الأوردرات وادخل على التفاصيل.
3. انسخ لينك الأوردر وافتحه من يوزر تاني (incognito) وورّي الـ 404.
