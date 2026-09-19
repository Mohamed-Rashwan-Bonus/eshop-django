# عضو 1 — قائد الفريق والتأسيس (Setup)

## 1. مهمتك ايه بالظبط
انت اللي أسست المشروع كله والباقي بنا فوق شغلك. مسؤول عن:
- إنشاء مشروع Django والـ apps الأربعة
- ملف الإعدادات `config/settings.py` (الداتابيز، اليوزر، الملفات)
- توزيع الروابط `config/urls.py` والصفحة الرئيسية
- نظام Git والدمج (merge) بتاع الفريق

## 2. المفاهيم اللي لازم تعرف تشرحها
- MVT يعني Model (الداتا) + View (المنطق) + Template (الشكل). الفرق عن MVC ان الـ View عندنا هي اللي فيها المنطق والـ Template هي العرض.
- الـ virtual environment (venv) يعني بيئة معزولة للمكتبات عشان نسخ المكتبات متتعارضش مع مشاريع تانية.
- الـ migration يعني ترجمة الموديلز لجداول داتابيز بخطوتين: makemigrations (تجهيز) ثم migrate (تنفيذ).

## 3. الملفات بتاعتك سطر بسطر
### إنشاء المشروع (الأوامر اللي نفذتها)
```
py -m venv venv
pip install django pillow python-decouple "psycopg[binary]"
django-admin startproject config .
python manage.py startapp accounts
python manage.py startapp catalog
python manage.py startapp cart
python manage.py startapp orders
```

### config/settings.py — أهم 5 حاجات
```
INSTALLED_APPS = [..., 'accounts', 'catalog', 'cart', 'orders']
AUTH_USER_MODEL = 'accounts.CustomUser'
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = 'media/' ; MEDIA_ROOT = BASE_DIR / 'media'
```
- سجلت التطبيقات الأربعة عشان Django يشوفها.
- قلت له ان اليوزر بتاعنا مخصص مش الجاهز.
- عرفت مكان القوالب والـ CSS والصور المرفوعة.

### الداتابيز المزدوجة (نقطة قوة في المناقشة)
```
if env('DB_ENGINE', default='sqlite') == 'postgresql':
    DATABASES = {...postgres...}
else:
    DATABASES = {...sqlite...}
```
- بنفس الكود المشروع يشتغل على SQLite (للتجربة السريعة) وPostgreSQL (للتسليم).
- الباسورد بره الكود في ملف `.env` اللي مش بيترفع على GitHub.

### config/urls.py — بوابة الموقع
```
path('admin/', admin.site.urls),
path('', home, name='home'),
path('shop/', include('catalog.urls')),
path('accounts/', include('accounts.urls')),
path('cart/', include('cart.urls')),
path('orders/', include('orders.urls')),
```
- كل app ليه ملف روابط خاص بيه، وانت جمعتهم هنا.

## 4. انت مربوط بمين
- عضو 2 (Auth): هو اللي عمل CustomUser وانت اللي فعلته في settings.
- عضو 3 (Models): هو عمل الجداول وانت عملت له migrate.
- عضو 7 (Frontend): استلم منك base.html الفاضية وملاها.
- عضو 8 (QA): بيجرب على التأسيس بتاعك.

## 5. أسئلة مناقشة متوقعة
- س: ليه فصلتوا 4 تطبيقات مش تطبيق واحد؟ ج: عشان كل عضو يشتغل لوحده من غير تعارض، وكل تطبيق مسؤول عن دومين واحد (auth / catalog / cart / orders).
- س: لو PostgreSQL وقعت هتعمل ايه؟ ج: نغير سطر واحد في .env لـ sqlite والمشروع يقوم فورا.
- س: الـ SECRET_KEY والباسورد فين؟ ج: في .env بره الكود وبره GitHub.
- س: ايه الفرق بين STATIC و MEDIA؟ ج: static ملفاتنا الثابتة (CSS/JS)، وmedia ملفات المستخدمين (صور المنتجات).

## 6. العرض اللايف بتاعك (دقيقتين)
1. افتح `settings.py` وورّي التبديل بين الداتابيزتين.
2. نفذ `python manage.py check` وورّي ان مفيش مشاكل.
3. افتح `/admin/` وورّي كل الجداول متسجلة.
