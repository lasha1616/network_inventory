# Network Inventory

A Django REST Framework application for managing network equipment across multiple city locations (headquarters and branches). Includes a clean single-page HTML frontend, token-based authentication, and role-based access control.

---

## Features

- **Cities → Locations → Equipment** hierarchy with full CRUD
- Each location (HQ or Branch) can hold any number of routers, switches, access points, etc.
- Equipment tracked by: type, brand, model, IP address, MAC address, serial number, inventory number
- **Admin users** can create, update and delete everything including cities, locations and users
- **Regular users** can add equipment and manage only their own entries (edit/delete)
- Ownership tracking — every equipment entry shows who created it
- Token authentication (DRF `authtoken`) — auto-assigned on user creation
- Django admin panel at `/admin/`
- Browsable DRF API at `/api/`
- Single-page HTML dashboard at `/`
- Quick links to Admin Panel, API Browser and API Login on both login screen and dashboard header
- Production-ready with Gunicorn + WhiteNoise for static files
- PostgreSQL support (SQLite3 used by default for development)
- Reverse proxy ready (tested with Nginx Proxy Manager + OPNsense)

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
│   ├── urls.py
│   └── wsgi.py
└── inventory/                  ← Main application
    ├── models.py               ← City, Location, NetworkEquipment
    ├── serializers.py
    ├── views.py                ← DRF ViewSets + custom login view
    ├── urls.py                 ← API router
    ├── permissions.py          ← IsAdminOrReadOnly, IsAdminOrOwner
    ├── admin.py
    ├── frontend_urls.py        ← Serves the HTML dashboard
    └── templates/
        └── inventory/
            └── index.html      ← Single-page frontend
```

---

## Data Model

```
City
 └── Location (HQ / Branch)
      ├── street, building_number
      └── NetworkEquipment (Router / Switch / AP / Other)
           ├── brand, model_name
           ├── ip_address, mac_address
           ├── serial_number, inventory_number
           ├── notes
           └── created_by (User)
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,your-server-ip

USE_POSTGRES=False

DB_NAME=network_inventory
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```