# gunicorn.conf.py
# Run with: gunicorn -c gunicorn.conf.py network_inventory.wsgi:application

import multiprocessing

# ── Binding ───────────────────────────────────────────────────
bind = "0.0.0.0:8000"

# ── Workers ───────────────────────────────────────────────────
# Rule of thumb: (2 × CPU cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120

# ── Logging ───────────────────────────────────────────────────
accesslog = "-"    # stdout
errorlog  = "-"    # stderr
loglevel  = "info"

# ── Process naming ────────────────────────────────────────────
proc_name = "network_inventory"

# ── Restart on code change (dev only — remove in production) ──
# reload = True
