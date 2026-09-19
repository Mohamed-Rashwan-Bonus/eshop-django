# عضو 3 — الموديلز ولوحة الأدمن (Categories + Products) — الشروط 10 ل 24

## 1. مهمتك ايه بالظبط
تصميم الجداول (Category و Product) وتسجيلها في Django Admin عشان الأدمن يضيف ويعدل ويمسح. ملفاتك: `catalog/models.py` و `catalog/admin.py`.

## 2. المفاهيم اللي لازم تعرف تشرحها
- الـ Model يعني كلاس بيمثل جدول: كل attribute عمود، وكل object صف.
- الـ ForeignKey يعني علاقة (منتج واحد ينتمي لكاتيجوري واحدة) — شرط 14.
- on_delete=PROTECT يعني ممنوع تمسح الأب لو عنده أولاد (حماية شرط 12).
- الـ slug يعني نسخة نظيفة من الاسم للروابط (مثلا iPhone 15 تبقى iphone-15).
- Pillow مكتبة إجبارية عشان حقل الصور ImageField يشتغل.

## 3. الملفات بتاعتك سطر بسطر
### catalog/models.py — الجدولان
```
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
```
```
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    discount_percent = models.PositiveIntegerField(default=0, validators=[0..100])
    is_active = models.BooleanField(default=True)
```
- شرط 18 ل 24: كل حقل مطلوب موجود (اسم، وصف، سعر عشري دقيق، مخزون، صورة، كاتيجوري، حالة نشط).
- السعر Decimal مش float عشان الفلوس متحصلش فيها أخطاء تقريب.
- image_url اتضافت عشان الـ 150 منتج الحقيقي صورهم على CDN من غير ما نحمل 30 ميجا.
- الـ slug بيتولد لوحده، ولو اتكرر (حصل فعلا مع منتجين) بياخد رقم -2 و -3 تلقائيا.

### catalog/admin.py — لوحة التحكم
```
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_percent', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    list_editable = ('price', 'discount_percent', 'stock', 'is_active')
```
- شرط 15 و16 و17: الإنشاء والتعديل والمسح من الأدمن.
- list_editable بتخلي الأدمن يغير السعر والخصم والمخزون من الليست نفسها بسرعة.
- شرط 12 (طبقة تانية فوق PROTECT): لو حاولت تمسح كاتيجوري فيها منتجات من الأدمن بيشوف رسالة منع بدل خطأ.

## 4. انت مربوط بمين
- عضو 4: بياخد الموديلز بتاعتك يعرضها للزبون (active بس).
- عضو 5 و6: بيقروا stock و price و current_price من عندك.
- عضو 1: عمل لك migrate للجداول دي.

## 5. أسئلة مناقشة متوقعة
- س: ليه PROTECT مش CASCADE؟ ج: عشان مسح كاتيجوري بالغلط ميمسحش كل منتجاتها — المطلوب (شرط 12) المنع مش المسح المتسلسل.
- س: ليه Decimal للسعر؟ ج: الـ float بيغلط في الكسور (0.1+0.2) ومينفعش في الفلوس.
- س: الصورة بتتخزن فين؟ ج: الملف في فولدر media/products والـ path بس في الداتابيز، ولازم Pillow.
- س: slug مكرر حصل ازاي واتحل؟ ج: منتجين أسمائهم بتتنضف لنفس الـ slug، والـ save بقت تجرب -2 و -3 لحد ما تلاقي الفاضي.

## 6. العرض اللايف بتاعك (دقيقتين)
1. من الأدمن ضيف كاتيجوري ومنتج جديد بصورة.
2. حاول تمسح كاتيجوري فيها منتجات وورّي رسالة المنع.
3. غير خصم منتج من الليست وورّي السعر اتغير في الموقع.
