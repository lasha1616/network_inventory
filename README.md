# Network Inventory

A production-ready Django REST Framework application for managing network equipment across multiple city locations (headquarters and branches). Includes a clean single-page HTML frontend, token-based authentication, role-based access control, interactive API documentation, and pagination.

🌐 **Live demo:** [https://drf.itdev.ge](https://drf.itdev.ge)

---

## Features

- **Cities → Locations → Equipment** hierarchy with full CRUD
- Each location (HQ or Branch) can hold any number of routers, switches, access points, etc.
- Equipment tracked by: type, brand, model, IP address, MAC address, serial number, inventory number
- **Admin users** — full CRUD on everything including cities, locations, users and equipment
- **Regular users** — read everything, add equipment, edit/delete only their own entries
- Ownership tracking — every equipment entry shows who created it
- Token authentication (DRF `authtoken`) — token auto-assigned on user creation
- Pagination — 5 items per page on all list endpoints
- Interactive API docs with **Swagger UI** at `/swagger/`
- Clean read-only API docs with **ReDoc** at `/redoc/`
- Django admin panel at `/admin/`
- Browsable DRF API at `/api/`
- Single-page HTML dashboard at `/`
- Quick links to Admin Panel, API Browser, API Login, Swagger, ReDoc and GitHub on both login screen and dashboard header
- Production-ready with **Gunicorn** + **WhiteNoise** for static files
- PostgreSQL support (SQLite3 used by default for development)
- Reverse proxy ready (tested with Nginx Proxy Manager + OPNsense)

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend framework | Django 5.0 |
| REST API | Django REST Framework 3.16 |
| Database | PostgreSQL (SQLite3 for dev) |
| Production server | Gunicorn 25.1 |
| Static files | WhiteNoise 6.12 |
| API documentation | drf-spectacular (Swagger + ReDoc) |
| Authentication | DRF Token Authentication |
| Process manager | systemd |
| Reverse proxy | Nginx Proxy Manager |

---

## Quick Start (SQLite3)

```bash
# 1. Clone and enter the project
git clone https://github.com/lasha1616/network_inventory.git
cd network_inventory

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env — at minimum change SECRET_KEY

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (admin)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver

# Open http://127.0.0.1:8000
```

---

## Switching to PostgreSQL

1. Install the driver (already in requirements.txt):
   ```bash
   pip install psycopg2-binary
   ```

2. Create the database in PostgreSQL:
   ```sql
   CREATE DATABASE network_inventory;
   CREATE USER network_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE network_inventory TO network_user;
   ```

3. Edit `.env`:
   ```
   USE_POSTGRES=True
   DB_NAME=network_inventory
   DB_USER=network_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Re-run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser again (fresh database):
   ```bash
   python manage.py createsuperuser
   ```

---

## Running with Gunicorn (Production)

```bash
# Collect static files first
python manage.py collectstatic

# Run using the included config file
gunicorn -c gunicorn.conf.py network_inventory.wsgi:application

# Or run directly
gunicorn network_inventory.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

> **Before going to production** set these in `.env`:
> ```
> DEBUG=False
> ALLOWED_HOSTS=yourdomain.com,your-server-ip
> ```

---

## Running as a systemd Service (Recommended)

Create `/etc/systemd/system/network_inventory.service`:

```ini
[Unit]
Description=Network Inventory Gunicorn Service
After=network.target

[Service]
User=youruser
Group=youruser
WorkingDirectory=/var/www/network_inventory
Environment="PATH=/var/www/network_inventory/venv/bin"
ExecStart=/var/www/network_inventory/venv/bin/gunicorn -c gunicorn.conf.py network_inventory.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable network_inventory
sudo systemctl start network_inventory
sudo systemctl status network_inventory
```

---

## Reverse Proxy (Nginx Proxy Manager)

If you are using Nginx Proxy Manager, add these headers in the **Advanced** tab:

```nginx
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

Also update `.env`:
```
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,your-server-ip
```

---

## API Documentation

| URL | Description |
|-----|-------------|
| `/swagger/` | Interactive Swagger UI — test endpoints directly in browser |
| `/redoc/` | Clean ReDoc documentation — great for sharing with others |
| `/api/schema/` | Raw OpenAPI 3.0 schema (JSON) |

### How to authenticate in Swagger
1. Go to `/swagger/`
2. Use `POST /api/auth/login/` — enter your username and password — copy the token
3. Click **Authorize** 🔒 at the top right
4. In the `tokenAuth` field enter: `Token your_token_here`
5. Click **Authorize** → **Close**

---

## API Endpoints

| Method | URL | Description | Who can use |
|--------|-----|-------------|-------------|
| POST | `/api/auth/login/` | Get auth token | Anyone |
| GET | `/api/cities/` | List all cities | Authenticated |
| POST | `/api/cities/` | Create city | Admin only |
| GET/PATCH/DELETE | `/api/cities/{id}/` | Detail/update/delete | Admin for write |
| GET | `/api/locations/` | List locations | Authenticated |
| POST | `/api/locations/` | Create location | Admin only |
| GET/PATCH/DELETE | `/api/locations/{id}/` | Detail/update/delete | Admin for write |
| GET | `/api/equipment/` | List all equipment | Authenticated |
| POST | `/api/equipment/` | Add equipment | Authenticated |
| GET/PATCH/DELETE | `/api/equipment/{id}/` | Detail/update/delete | Admin or owner |
| GET | `/api/users/` | List users | Admin only |
| POST | `/api/users/` | Create user | Admin only |
| GET | `/api/users/me/` | Current user info | Authenticated |

### Pagination

All list endpoints return paginated results — 5 items per page:

```json
{
    "count": 20,
    "next": "http://yourdomain/api/equipment/?page=2",
    "previous": null,
    "results": [...]
}
```

### Filter parameters

```
/api/locations/?city=1         — filter by city ID
/api/locations/?type=HQ        — filter by type (HQ or BR)
/api/equipment/?location=2     — filter by location ID
/api/equipment/?type=router    — filter by type (router, switch, ap, other)
```

---

## Permission Model

| Action | Admin | Regular User |
|--------|-------|--------------|
| View everything | ✅ | ✅ |
| Add City / Location | ✅ | ❌ |
| Add Equipment | ✅ | ✅ |
| Edit / Delete own equipment | ✅ | ✅ |
| Edit / Delete others' equipment | ✅ | ❌ |
| Manage users | ✅ | ❌ |
| Access admin panel | ✅ | ❌ |

---

## Project Structure

```
network_inventory/
├── manage.py
├── gunicorn.conf.py            ← Gunicorn configuration
├── requirements.txt
├── .env.example                ← Copy to .env (never commit .env!)
├── .gitignore
├── README.md
├── network_inventory/          ← Django project config
│   ├── settings.py             ← SQLite3 by default, flip one flag for PostgreSQL
│   ├── urls.py                 ← Root URLs including Swagger and ReDoc
│   └── wsgi.py
└── inventory/                  ← Main application
    ├── models.py               ← City, Location, NetworkEquipment
    ├── serializers.py          ← DRF serializers with nested relations
    ├── views.py                ← ModelViewSets + custom login view
    ├── urls.py                 ← API router
    ├── permissions.py          ← IsAdminOrReadOnly, IsAdminOrOwner
    ├── admin.py                ← Admin panel with save_model override
    ├── frontend_urls.py        ← Serves the HTML dashboard
    └── templates/
        └── inventory/
            └── index.html      ← Single-page frontend (vanilla JS)
```

---

## Data Model

```
City
 └── Location (HQ / Branch)
      ├── name, street, building_number
      └── NetworkEquipment (Router / Switch / AP / Other)
           ├── brand, model_name
           ├── ip_address, mac_address
           ├── serial_number, inventory_number
           ├── notes
           └── created_by (FK → User)
```

---

## Architecture

This is a **monolithic** Django application — the backend (API) and frontend (HTML dashboard) are served by the same Django process:

```
Browser
  └── https://yourdomain.com/
        ├── /              → Single-page HTML dashboard (TemplateView)
        ├── /api/          → REST API (DRF ModelViewSets)
        ├── /admin/        → Django admin panel
        ├── /swagger/      → Swagger UI (drf-spectacular)
        └── /redoc/        → ReDoc documentation (drf-spectacular)
```

The frontend uses **Token Authentication** via `localStorage` — completely independent from the Django session used by the admin panel. This means you can be logged in as different users on the dashboard and the admin panel simultaneously.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,your-server-ip

USE_POSTGRES=False

DB_NAME=network_inventory
DB_USER=network_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```