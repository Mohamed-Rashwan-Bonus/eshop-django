# E-Shop — Django MVT E-Commerce (Final Project, Team of 8)

Customers browse products, search & filter, view details, add to a session cart,
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
python manage.py seed         # 4 categories + 10 demo products
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

## 3) Team of 8 → who owns what (PDF 1–54)
| # | Person | App | Requirements |
|---|--------|-----|--------------|
| 1 | Lead / setup | `config` | settings, urls, base layout, merges |
| 2 | Auth | `accounts` | 1–9: register/login/logout/profile, EG phone |
| 3 | Models+Admin | `catalog` | 10–24: Category/Product, PROTECT rule |
| 4 | Catalog UI | `catalog` | 25–31: list/detail/search/filter/sort |
| 5 | Cart | `cart` | 32–41: session cart, stock guard |
| 6 | Checkout+Orders | `orders` | 42–54: order, stock-, history, privacy |
| 7 | Frontend/UX | templates+static | Bootstrap 5, badges, toasts, responsive |
| 8 | QA/DB/Docs | — | test all 54, `seed`, README, demo |

> `.env`, `venv/` and `media/` are never committed (see `.gitignore`) — each machine generates its own via `setup.bat`.

## 4) Design notes (2026 UX best practices)
Sticky navbar with live search (`/` focuses it) + cart badge, scannable cards with
New / Low-stock / Out-of-stock badges + quick-add, visible active filters with one-click
clear, guided Cart → Checkout → Done steps, single-page checkout with live order review,
toasts instead of page reloads, trust strip (shipping/secure/returns) everywhere.
