# عضو 4 — عرض المنتجات والبحث (Catalog UI) — الشروط 25 ل 31

## 1. مهمتك ايه بالظبط
الصفحات اللي الزبون بيشوفها: ليستة المنتجات + صفحة التفاصيل + البحث والفلترة والترتيب. ملفاتك: `catalog/views.py` (دوال العرض) والقوالب بتاعتها.

## 2. المفاهيم اللي لازم تعرف تشرحها
- الـ QuerySet يعني استعلام لسه متنفذش — بنركب عليه فلاتر ورا بعض وبعدين يتنفذ مرة واحدة (كفاءة).
- `icontains` يعني بحث غير حساس لحالة الحروف (hp تلاقي HP).
- الـ context يعني القاموس اللي الـ view بتبعته للقالب (products و categories).
- get_object_or_404 يعني هات المنتج او صفحة 404 — وده بيحقق إخفاء المنتجات المطفية.

## 3. الملفات بتاعتك سطر بسطر
### catalog/views.py — product_list
```
products = Product.objects.filter(is_active=True).select_related('category')
if q:
    products = products.filter(name__icontains=q)          # شرط 27
if cat:
    products = products.filter(category__slug=cat)         # شرط 28
if min_price:
    products = products.filter(price__gte=min_price)       # شرط 29
if max_price:
    products = products.filter(price__lte=max_price)
if ordering in ('price', '-price', 'name', '-name'):       # شرط 30
    products = products.order_by(ordering)
```
- شرط 25: السطر الأول بيجيب النشط بس — المطفي مش بيظهر أبدا.
- select_related بتجيب الكاتيجوري مع المنتج في استعلام واحد بدل 150 استعلام.
- كل الفلاتر اختيارية وبتتركب فوق بعض.

### product_detail
```
product = get_object_or_404(Product, slug=slug, is_active=True)   # شرط 26
related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
```
- لو المنتج مطفي او مش موجود: 404 تلقائيا.
- related يعني منتجات مقترحة من نفس الكاتيجوري.

### cover_url في الموديل (بتستخدمها انت)
```
if self.image: return self.image.url
if self.image_url: return self.image_url
return picsum placeholder
```
- أولوية: صورة مرفوعة، ثم صورة حقيقية من CDN، ثم placeholder.

## 4. انت مربوط بمين
- عضو 3: الموديلز اللي بتعرضها.
- عضو 7: صمم لك الكروت والفلاتر وانت مليتها بالداتا.
- عضو 5: زرار Add to cart اللي في كروتك بيروح عنده.

## 5. أسئلة مناقشة متوقعة
- س: المنتج المطفي (inactive) بيظهر فين؟ ج: في حتة — الليست بتجيب active بس والتفاصيل بترجع 404.
- س: البحث شغال ازاي؟ ج: name__icontains على الاسم، والفلترة على slug الكاتيجوري والسعر، والترتيب بقيم مسموحة بس (عشان محدش يحقن ordering غريب).
- س: لو مفيش نتائج؟ ج: شرط 31 — القالب فيه empty state برسالة لطيفة وزرار يعرض الكل.
- س: select_related لازمتها ايه؟ ج: من غيرها كل منتج كان هيعمل استعلام للكاتيجوري (N+1 problem).

## 6. العرض اللايف بتاعك (دقيقتين)
1. دور على hp وورّي النتائج، وبعدين دور على حاجة مش موجودة وورّي الرسالة.
2. فلتر بكاتيجوري + سعر + ترتيب من الأرخص.
3. افتح منتج وورّي المقترحات من نفس الكاتيجوري.
