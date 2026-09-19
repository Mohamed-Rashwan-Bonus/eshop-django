# عضو 3 — الموديلز ولوحة الأدمن (Categories + Products) — الشروط 10 ل 24

## 1. مهمتك ايه بالظبط
تصميم الجداول (Category و Product) وتسجيلها في Django Admin عشان الأدمن يضيف ويعدل ويمسح. ملفاتك: catalog/models.py و catalog/admin.py.

## 2. من الصفر خالص: يعني ايه اللي انت عملته
- الـ Model يعني كلاس بايثون عادي بس Django بيفهمه كجدول: كل سطر فيه (attribute) بيبقى عمود، وكل object بتعمله بيبقى صف في الجدول.
- الـ ForeignKey يعني علاقة: كل منتج شايل رقم الكاتيجوري بتاعته. زي ان كل طالب شايل رقم الفصل بتاعه.
- on_delete=PROTECT يعني قانون حماية: ممنوع تمسح الكاتيجوري لو لسه فيها منتجات. البديل المرعب كان CASCADE اللي كان هيمسح المنتجات معاها.
- الـ slug يعني نسخة نظيفة من الاسم للروابط: iPhone 15 تبقى iphone-15 عشان الرابط يبقى شكله حلو.
- Pillow مكتبة بايثون إجبارية: من غيرها Django ميعرفش يتعامل مع الصور خالص.

## 3. قاموس المصطلحات بتاعتك
- CharField: نص قصير (اسم). TextField: نص طويل (وصف). DecimalField: فلوس بدقة. PositiveIntegerField: رقم صحيح موجب (مخزون وخصم).
- BooleanField: صح او غلط (نشط ولا مطفي).
- ImageField: صورة بتتخزن كملف، والداتابيز بتحفظ الـ path بس.
- related_name: الاسم اللي بتنادي بيه أولاد العلاقة (category.products يعني منتجات الكاتيجوري).
- ModelAdmin: كلاس بيتحكم في شكل الجدول جوه لوحة الأدمن.

## 4. الكود سطر بسطر
### catalog/models.py — جدول الكاتيجوري
```
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
```
- اسم الكاتيجوري وحيد (مفيش كاتيجوريين بنفس الاسم).
```
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
```
- الـ slug بيتولد لوحده من الاسم قبل الحفظ. super().save() هي اللي بتحفظ فعلا — احنا حشرنا خطوتنا قبلها.

### جدول المنتج (الشروط 18 ل 24)
```
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
```
- شرط 14: كل منتج ليه كاتيجوري واحدة إجباري. وPROTECT بتحقق شرط 12 (المنع بدل المسح المتسلسل).
```
    price = models.DecimalField(max_digits=10, decimal_places=2)
```
- فلوس بدقة رقمين عشريين. مش float عشان الـ float بيغلط في الكسور (جرب 0.1 + 0.2 على الآلة).
```
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True)
```
- المخزون ميبقاش بالسالب. الصورة إما ملف مرفوع في media/products أو لينك خارجي (بتاعة الـ 150 منتج الحقيقي).
```
    discount_percent = models.PositiveIntegerField(default=0, validators=[0..100])
    is_active = models.BooleanField(default=True)
```
- الخصم من 0 لـ 100، والصفر معناه مفيش خصم. والمطفي (False) الزبون ميشوفوش خالص.
- الـ slug المكرر: حصل فعلا مع منتجين أسمائهم بتتنضف لنفس الـ slug، والـ save بقت تجرب 2 و 3 لحد ما تلاقي الفاضي.

### catalog/admin.py (الشروط 10 و 11 و 15 و 16 و 17)
```
list_display = ('name', 'category', 'price', 'discount_percent', 'stock', 'is_active')
list_editable = ('price', 'discount_percent', 'stock', 'is_active')
list_filter = ('category', 'is_active')
search_fields = ('name',)
```
- الأعمدة اللي ظاهرة في الليست. والـ list_editable بتخلي الأدمن يغير السعر والخصم والمخزون من الليست نفسها من غير ما يفتح المنتج.
- شرط 12 (طبقة تانية): دالة delete_queryset بتمنع مسح أي كاتيجوري فيها منتجات برسالة واضحة.

## 5. مربوط بمين
- عضو 4: بيعرض الموديلز بتاعتك للزبون (النشط بس).
- عضو 5 و 6: بيقروا stock و current_price من عندك لحظيا.
- عضو 1: عمل لك migrate للجداول دي.

## 6. فيديوهات تذاكر منها
- Corey Schafer: حلقة Database and Migrations وحلقة Admin (أرقام 5 و 6) من نفس السلسلة:
- https://www.youtube.com/playlist?list=PLLtIxaRk6P3JRiiW1SAV2BLhuuSSCULRn
- كورس Django كامل بالعربي (Programming Secrets) — فيه الموديلز والأدمن:
- https://www.youtube.com/playlist?list=PLp2eAGIFKMEVnAAJWhGzLc1Nn-tFP1UHP
- شرح الموديلز والعلاقات مكتوب بالعربي:
- https://thecodefix.net/learn/django/00-intro

## 7. أسئلة مناقشة متوقعة
- س: ليه PROTECT مش CASCADE؟ ج: مسح كاتيجوري بالغلط ميمسحش منتجاتها — المطلوب المنع.
- س: ليه Decimal للسعر؟ ج: الـ float بيغلط في الكسور ومينفعش في الفلوس.
- س: الصورة بتتخزن فين؟ ج: الملف في media/products والـ path بس في الداتابيز، ولازم Pillow.
- س: slug مكرر اتحل ازاي؟ ج: الـ save بتجرب رقم زيادة لحد ما تلاقي slug فاضي.

## 8. العرض اللايف بتاعك
1. من الأدمن ضيف كاتيجوري ومنتج جديد بصورة.
2. حاول تمسح كاتيجوري فيها منتجات وورّي رسالة المنع.
3. غير خصم منتج من الليست وورّي السعر اتغير في الموقع.
