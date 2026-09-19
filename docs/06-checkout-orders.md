# عضو 6 — الدفع والأوردرات (Checkout + Orders) — الشروط 42 ل 54

## 1. مهمتك ايه بالظبط
أخطر جزء في المشروع: تحويل السلة لأوردر حقيقي + تقليل المخزون + تاريخ الأوردرات. الغلطة هنا يعني فلوس ضايعة. ملفاتك: orders/models.py و orders/views.py و orders/forms.py.

## 2. من الصفر خالص: يعني ايه اللي انت عملته
- الـ transaction.atomic يعني صفقة واحدة: يا كل الخطوات تنجح مع بعض (أوردر + أصناف + نقص مخزون + تفريغ سلة) يا كلها تتلغي. مينفعش أوردر يتعمل من غير ما المخزون ينقص.
- `F('stock') - qty` يعني الخصم بيحصل جوه الداتابيز نفسها مش في بايثون. الفرق مهم: لو اتنين اشتروا آخر قطعة في نفس الثانية، الداتابيز بترتبهم واحد واحد.
- حساب المجموع على السيرفر (شرط 45) يعني منثقش في أي رقم جاي من المتصفح، لأن أي حد يقدر يعدل HTML ويبعت total مزيف.
- سعر لحظة الشراء بيتخزن في OrderItem: لو سعر المنتج اتغير بعد شهر، الفاتورة القديمة تفضل صح.

## 3. قاموس المصطلحات بتاعتك
- atomic: يا الكل يا مفيش (ضمان سلامة العمليات).
- F expression: عملية حسابية بتتنفذ جوه الداتابيز.
- commit=False: جهز الـ object من الفورم من غير حفظ عشان تكمل بياناته (اليوزر والمجموع) وبعدين احفظ.
- rollback: التراجع عن كل حاجة حصلت جوه الصفقة.
- related_name: اسم الوصول العكسي (order.items يعني أصناف الأوردر).

## 4. الكود سطر بسطر
### orders/models.py
```
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER, on_delete=models.CASCADE, related_name='orders')
```
- كل أوردر مربوط بصاحبه. لو اليوزر اتمسح أوردراته تتمسح معاه (CASCADE هنا صح لأن الأوردر ملكه).
```
    full_name, email, phone, address, city
```
- بيانات الشحن اللي الزبون كتبها (شرط 43).
```
    total = models.DecimalField(...)
    created_at = models.DateTimeField(auto_now_add=True)
```
- المجموع محسوب على السيرفر (شرط 45) والتاريخ تلقائي.
```
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name, price, quantity
```
- SET_NULL عشان لو منتج اتمسح بعد البيع، الأوردر يفضل موجود باسمه وسعره. والسعر هنا هو سعر لحظة الشراء (شرط 47).

### checkout (الشروط 42 ل 50)
```
@login_required
```
- شرط 42: الأعضاء بس. الزائر بيتحول للدخول.
```
    cart = Cart(request)
    if len(cart) == 0: redirect
```
- سلة فاضية ملهاش checkout.
```
    form = CheckoutForm(request.POST or None)
```
- فورم الشحن، وجنبها الزبون بيراجع أصنافه قبل التأكيد (شرط 43 و 44).
```
        with transaction.atomic():
            total = cart.total()
            order = form.save(commit=False)
            order.user = request.user
            order.total = total
            order.save()
```
- شرط 45 و 46: المجموع من السيرفر والأوردر بيتعمل بصاحبه ومجموعه.
```
            for line in cart.items():
                if line['qty'] > p.stock: rollback + رسالة
                OrderItem.objects.create(... price=p.current_price ...)
                Product.objects.filter(pk=p.pk).update(stock=F('stock') - qty)
            cart.clear()
        return redirect('orders:confirmation', ...)
```
- شرط 47: الأصناف بسعر الخصم. شرط 48: نقص المخزون جوه الداتابيز. شرط 49: تفريغ السلة. شرط 50: تحويل لصفحة التأكيد.
- لو صنف خلص أثناء الدفع: rollback لكل حاجة ورسالة واضحة.

### history و detail (الشروط 51 ل 54)
```
Order.objects.filter(user=request.user)
```
- شرط 51: تاريخ أوردراتي أنا بس.
```
get_object_or_404(Order, id=order_id, user=request.user)
```
- شرط 54: أوردر حد تاني = 404 حتى لو خمنت الرقم. واتجربت فعلا.
- شرط 52 و 53: صفحة التفاصيل فيها الرقم والتاريخ والأصناف والكميات والأسعار والمجموع.

## 5. مربوط بمين
- عضو 2: request.user هو صاحب الأوردر.
- عضو 5: بتستلم السلة وتصفرها وبنفس سعرها.
- عضو 3: بتنقص الـ stock بتاعه.

## 6. فيديوهات تذاكر منها
- سلسلة متجر Django لـ Dennis Ivy (فيها الـ checkout والأوردرات):
- https://www.youtube.com/c/dennisivy
- كورس Django كامل بالعربي (Programming Secrets):
- https://www.youtube.com/playlist?list=PLp2eAGIFKMEVnAAJWhGzLc1Nn-tFP1UHP

## 7. أسئلة مناقشة متوقعة
- س: اتنين اشتروا آخر قطعة مع بعض؟ ج: الـ transaction والـ F بيخلوا واحد ينجح والتاني يشوف رسالة.
- س: ليه المجموع من السيرفر؟ ج: أي حد يقدر يعدل HTML المتصفح ويبعت total مزيف.
- س: منتج اتمسح بعد ما اتباع؟ ج: الأوردر محفوظ باسمه وسعره فالفاتورة سليمة.
- س: إزاي منعت رؤية أوردرات الغير؟ ج: كل استعلام فيه user=request.user، واتجربت بـ 404.

## 8. العرض اللايف بتاعك
1. اعمل checkout كامل وورّي صفحة التأكيد.
2. افتح تاريخ الأوردرات وادخل على التفاصيل.
3. انسخ لينك الأوردر وافتحه من يوزر تاني وورّي الـ 404.
