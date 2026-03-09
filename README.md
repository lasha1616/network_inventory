# Network Inventory

A Django REST Framework application for managing network equipment across multiple city locations (headquarters and branches). Includes a clean single-page HTML frontend, token-based authentication, and role-based access control.

---

## Features

- **Cities → Locations → Equipment** hierarchy with full CRUD
- Each location (HQ or Branch) can hold any number of routers, switches, access points, etc.
- Equipment tracked by: type, brand, model, IP address, MAC address, serial number, inventory number
- **Admin users** can create, update and delete everything
- **Regular users** can only view data (read-only)
- Token authentication (DRF `authtoken`)
- Django admin panel at `/admin/`
- Browsable DRF API at `/api/`
- Single-page HTML dashboard at `/`

---

## Quick Start (SQLite3)

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd network_inventory

# 2. Create and activate a virtual environment
python -m venv venv
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

1. Install the driver:
   ```bash
   pip install psycopg2-binary
   ```
   Uncomment the `psycopg2-binary` line in `requirements.txt`.

2. Create the database in PostgreSQL:
   ```sql
   CREATE DATABASE network_inventory;
   ```

3. Edit `.env`:
   ```
   USE_POSTGRES=True
   DB_NAME=network_inventory
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Re-run migrations:
   ```bash
   python manage.py migrate
   ```

---

## Running with Gunicorn (Production)

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run using the included config file
gunicorn -c gunicorn.conf.py network_inventory.wsgi:application

# Or run directly
gunicorn network_inventory.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

> **Before going to production**, also set `DEBUG=False` and `ALLOWED_HOSTS` in `.env`, then run:
> ```bash
> python manage.py collectstatic
> ```

---

## API Endpoints

| Method | URL | Description | Auth required |
|--------|-----|-------------|---------------|
| POST | `/api/auth/login/` | Get auth token | No |
| GET | `/api/cities/` | List all cities | Yes |
| POST | `/api/cities/` | Create city | Admin |
| GET/PATCH/DELETE | `/api/cities/{id}/` | Detail/update/delete | Admin for write |
| GET | `/api/locations/` | List locations | Yes |
| POST | `/api/locations/` | Create location | Admin |
| GET/PATCH/DELETE | `/api/locations/{id}/` | Detail/update/delete | Admin for write |
| GET | `/api/equipment/` | List all equipment | Yes |
| POST | `/api/equipment/` | Add equipment | Admin |
| GET/PATCH/DELETE | `/api/equipment/{id}/` | Detail/update/delete | Admin for write |
| GET | `/api/users/` | List users | Admin |
| POST | `/api/users/` | Create user | Admin |
| GET | `/api/users/me/` | Current user info | Yes |

### Filter parameters

- `/api/locations/?city=1` — filter by city ID
- `/api/locations/?type=HQ` — filter by type (HQ or BR)
- `/api/equipment/?location=2` — filter by location ID
- `/api/equipment/?type=router` — filter by type (router, switch, ap, other)

---

## Project Structure

```
network_inventory/
├── manage.py
├── gunicorn.conf.py        ← Gunicorn configuration
├── requirements.txt
├── .env.example            ← Copy to .env (never commit .env!)
├── .gitignore
├── network_inventory/      ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── inventory/              ← Main application
    ├── models.py           ← City, Location, NetworkEquipment
    ├── serializers.py
    ├── views.py            ← DRF ViewSets
    ├── urls.py             ← API router
    ├── permissions.py      ← IsAdminOrReadOnly
    ├── admin.py
    └── templates/
        └── inventory/
            └── index.html  ← Single-page frontend
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
           └── notes
```
