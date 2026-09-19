# عضو 1 — قائد الفريق والتأسيس (Setup)

## 1. مهمتك ايه بالظبط
انت اللي بنيت الأرض اللي الكل وقف عليها. من غير شغلك مفيش حد يعرف يشتغل. مسؤول عن:
- إنشاء مشروع Django والـ apps الأربعة (accounts و catalog و cart و orders)
- ملف الإعدادات config/settings.py (الداتابيز واليوزر والملفات)
- توزيع الروابط config/urls.py والصفحة الرئيسية
- نظام Git: مين يشتغل فين وإزاي ندمج من غير ما نكسر شغل بعض

## 2. من الصفر خالص: يعني ايه اللي انت عملته
- تخيل انك بتبني مول: django-admin startproject يعني صب الخرسانة والأعمدة. startapp يعني تقسيم المحلات جواه.
- الـ app في Django يعني فولدر مستقل لجزء واحد من الموقع. فصلناهم 4 عشان كل واحد يشتغل لوحده من غير ما يلغبط التاني.
- الـ venv يعني أوضة مقفولة للمكتبات بتاعة المشروع ده بس. من غيرها نسخة Django بتاعة مشروع ممكن تبوظ مشروع تاني.
- الـ migration يعني خطوتين: الأولى makemigrations بتكتب خطة الجداول، والتانية migrate بتنفذها في الداتابيز فعلا.

## 3. قاموس المصطلحات بتاعتك
- MVT: طريقة تقسيم الشغل (Model للداتا، View للمنطق، Template للشكل).
- settings.py: ملف إعدادات المشروع كله.
- INSTALLED_APPS: الليستة اللي بتقول لـ Django التطبيقات الشغالة.
- AUTH_USER_MODEL: تعريف مين هو اليوزر بتاعنا.
- STATIC: ملفاتنا الثابتة (CSS و JS). MEDIA: ملفات المستخدمين (صور المنتجات).
- .env: ملف الأسرار (باسورد الداتابيز) وبره GitHub.
- merge: دمج شغل اتنين في نسخة واحدة.

## 4. الكود سطر بسطر
### أوامر التأسيس (نفذتها مرة واحدة بالترتيب)
```
py -m venv venv
```
- بيعمل فولدر venv فيه نسخة Python خاصة بالمشروع.
```
pip install django pillow python-decouple "psycopg[binary]"
```
- django هو الفريم وورك. pillow عشان صور المنتجات. psycopg عشان نكلم PostgreSQL. python-decouple عشان نقرا الأسرار من .env.
```
django-admin startproject config .
```
- بيعمل المشروع الأم. النقطة في الآخر معناها اعمله هنا مش في فولدر جديد.
```
python manage.py startapp accounts
python manage.py startapp catalog
python manage.py startapp cart
python manage.py startapp orders
```
- بيعمل الـ 4 محلات، وكل أمر بيطلع فولدر فيه models.py و views.py و admin.py فاضيين يتمليوا بعدين.

### config/settings.py (أهم 5 سطور)
```
INSTALLED_APPS = [..., 'accounts', 'catalog', 'cart', 'orders']
```
- بتسجل التطبيقات عشان Django يشوف جداولها وروابطها وقوالبها.
```
AUTH_USER_MODEL = 'accounts.CustomUser'
```
- بتقول له انسى اليوزر الجاهز، اليوزر بتاعنا اللي عمله عضو 2.
```
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = 'media/'
```
- أماكن القوالب والـ CSS وصور المنتجات المرفوعة.
```
if env('DB_ENGINE', default='sqlite') == 'postgresql':
```
- لو مكتوب postgresql في .env اشتغل على PostgreSQL، غير كده SQLite. نفس الكود شغال على الاتنين.

### config/urls.py (بوابة الموقع)
```
path('admin/', admin.site.urls),
path('', home, name='home'),
path('shop/', include('catalog.urls')),
path('accounts/', include('accounts.urls')),
path('cart/', include('cart.urls')),
path('orders/', include('orders.urls')),
```
- كل app ليه ملف روابط خاص، وانت جمعتهم هنا. أي رابط يبدأ بـ shop بيروح لعضو 4، وأي رابط accounts بيروح لعضو 2، وهكذا.

## 5. مربوط بمين
- عضو 2: فعلت له AUTH_USER_MODEL.
- عضو 3: عملت له migrate للجداول.
- عضو 7: استلم base.html الفاضية.
- عضو 8: بيجرب على التأسيس بتاعك.

## 6. فيديوهات تذاكر منها
- سلسلة Corey Schafer للـ Django من الصفر (أول حلقتين: التأسيس والـ apps):
- https://www.youtube.com/playlist?list=PLLtIxaRk6P3JRiiW1SAV2BLhuuSSCULRn
- كورس GIT بالعربي من قناة الزيرو (عشان الـ merge):
- https://www.youtube.com/@ElzeroWebSchool

## 7. أسئلة مناقشة متوقعة
- س: ليه 4 تطبيقات مش واحد؟ ج: عشان كل عضو يشتغل لوحده من غير تعارض، وكل تطبيق مسؤول عن دومين واحد.
- س: لو PostgreSQL وقعت؟ ج: سطر واحد في .env يبقى sqlite والمشروع يقوم فورا.
- س: الباسورد فين؟ ج: في .env بره الكود وبره GitHub.
- س: الفرق بين STATIC و MEDIA؟ ج: static ملفاتنا، وmedia صور المستخدمين.

## 8. العرض اللايف بتاعك
1. افتح settings.py وورّي التبديل بين الداتابيزتين.
2. نفذ python manage.py check وورّي ان مفيش مشاكل.
3. افتح /admin/ وورّي كل الجداول متسجلة.
