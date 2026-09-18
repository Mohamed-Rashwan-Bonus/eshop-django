# ملف السيطب الكامل — ابعته مع البروجيكت 📦

لو استلمت فولدر `ecommerce` ومش عارف تشغله، امشي على الخطوات دي واحدة واحدة.

## الطريقة السهلة (دابل كليك)
1. اتأكد ان **Python** متسطب من `python.org/downloads` (علّم على `Add python.exe to PATH` وانت بتسطب).
2. دابل كليك على **`setup.bat`** جوه فولدر المشروع.
3. هو هيعمل كل حاجة لوحده: بيئة افتراضية + مكتبات + داتابيز + داتا تجريبية، وفي الآخر هيفتح الموقع لوحده على `http://127.0.0.1:8000/`.
4. لو سألك `Create admin account now?` اكتب `Y` واعمل أكونت أدمن، أو دوس Enter وهيستخدم الديمو: `admin@test.com / admin12345`.

> ملحوظة: `setup.bat` بيحاول يشغل **PostgreSQL** الأول، ولو مش موجود عندك هيشغل SQLite مؤقتا عشان المشروع يقوم فورا. عشان ترجع لـ PostgreSQL شوف الجزء اللي تحت.

## الطريقة اليدوية (لو الأوتوماتيك وقف)
```powershell
cd ecommerce
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed
python manage.py createsuperuser
python manage.py runserver
```

## تشغيل PostgreSQL (عشان التدريب طالبها)
1. سطبها بأمر واحد: `winget install -e --id PostgresPro.Standard.17`
2. اتأكد السيرفس شغالة: اسمها `postgresql-X64-17`.
3. نفذ الأمرين دول (الباسورد `postgres`):
```powershell
psql -U postgres -h localhost -c "ALTER USER postgres WITH PASSWORD 'postgres';"
createdb -U postgres -h localhost ecommerce_db
```
4. في ملف `.env` خلي `DB_ENGINE=postgresql` و `DB_PASSWORD=postgres`، وبعدين `python manage.py migrate` + `python manage.py seed`.

## حسابات الديمو
| النوع | Email | Password |
|---|---|---|
| أدمن | admin@test.com | admin12345 |
| زبون | سجل واحد جديد من `/accounts/register/` | — |

## أشهر 3 مشاكل وحلها
1. **`python` بيفتح Microsoft Store:** استخدم `py` بدل `python`، أو فعّل الـ venv الأول بـ `.\venv\Scripts\activate`.
2. **اللوكال هوست مش شغال:** لازم تكون واقف **جوه فولدر `ecommerce`** اللي فيه `manage.py`، والـ venv متفعل (هتلاقي `(venv)` على الشمال).
3. **`migrate` بيقول connection failed:** يا PostgreSQL مش شغالة، يا الباسورد في `.env` غلط. `setup.bat` بيعديها لوحده بـ SQLite، وانت صلح الباسورد وارجع شغل `migrate` تاني.

## الرفع على GitHub
```powershell
git init
git add .
git commit -m "E-Shop final project"
git remote add origin https://github.com/<اسمك>/<الريبو>.git
git branch -M main
git push -u origin main
```
ملفات `.env` و `venv/` و `media/` مش بتترفع (موجودين في `.gitignore`) — واللي هيستلم هيعمل `.env` من `setup.bat` لوحده.
