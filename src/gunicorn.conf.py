import multiprocessing

# Server socket
bind: str = "0.0.0.0:5000"
backlog: int = 2048

# Worker processes
workers: int = multiprocessing.cpu_count() * 2 + 1
worker_class: str = "sync"
worker_connections: int = 1000
timeout: int = 30
keepalive: int = 2

# Restart workers after this many requests, with up to 50% jitter
max_requests: int = 1000
max_requests_jitter: int = 500

# Logging
accesslog: str = "-"
errorlog: str = "-"
loglevel: str = "info"
access_log_format: str = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name: str = "object-storage-api"

# Server mechanics
daemon: bool = False
pidfile: str = "/tmp/gunicorn.pid"
user: str = "root"
group: str = "root"
tmp_upload_dir: str = "/tmp"

# SSL (if needed)
# keyfile: str = "/path/to/keyfile"
# certfile: str = "/path/to/certfile"

# Security
limit_request_line: int = 4094
limit_request_fields: int = 100
limit_request_field_size: int = 8190

# Performance tuning
preload_app: bool = True
worker_tmp_dir: str = "/dev/shm"

# Graceful handling
graceful_timeout: int = 30
