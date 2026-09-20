# E-Shop — Django MVT E-Commerce

Built by Mohamed Rashwan — customers browse products, search & filter, view details, add to a session cart,
checkout with shipping info, and review order history. Admins manage everything in Django Admin.

## 1) Run it (Windows, 2 minutes)

**New machine? Just double-click `setup.bat`** — it installs everything and starts the server.
Full Arabic guide: `SETUP.md`.

Manual way:
```powershell
cd ecommerce
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env        # then edit .env (PostgreSQL password below)
python manage.py migrate
python manage.py createsuperuser
python manage.py seed         # 10 demo products - or: seed_real for 150 real products with photos
python manage.py runserver
```
Or just double-click **`run.bat`**.
- Store: http://127.0.0.1:8000/ — Admin: http://127.0.0.1:8000/admin/
- Demo admin: `admin@test.com` / `admin12345`

**Localhost not working?** You must run from inside the `ecommerce` folder
(the one containing `manage.py`) with the venv python:
`.\venv\Scripts\activate` then `python manage.py runserver`.
`python --version` failing means the venv isn't activated or you used the
Microsoft Store stub — use `py` or the `.\venv\Scripts\python.exe` path.

## 2) PostgreSQL (already configured)
- Server: `localhost:5432`, DB `ecommerce_db`, user/pass `postgres`/`postgres` (see `.env`)
- Install: `winget install -e --id PostgresPro.Standard.17`
- Start service `postgresql-X64-17` if needed, then:
  `psql -U postgres -h localhost -c "ALTER USER postgres WITH PASSWORD 'postgres';"`
  `createdb -U postgres -h localhost ecommerce_db`
- Switch engines anytime in `.env`: `DB_ENGINE=postgresql` or `sqlite`

## 3) Scope — اللي اتنفذ
`config` + `accounts` (register/login/logout/profile + تحقق رقم مصري) + `catalog` (Category/Product + بحث/فلترة) + `cart` (سلة session + حماية مخزون) + `orders` (checkout + سجل طلبات) + واجهة Bootstrap 5 + seed بـ 150 منتج.

> `.env`, `venv/` and `media/` are never committed (see `.gitignore`) — each machine generates its own via `setup.bat`.

## 4) Design notes (2026 UX best practices)
Sticky navbar with live search (`/` focuses it) + cart badge, scannable cards with
New / Low-stock / Out-of-stock badges + quick-add, visible active filters with one-click
clear, guided Cart → Checkout → Done steps, single-page checkout with live order review,
toasts instead of page reloads, trust strip (shipping/secure/returns) everywhere.
