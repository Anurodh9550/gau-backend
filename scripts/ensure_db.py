import os
from pathlib import Path

import psycopg2
from psycopg2 import sql

# Resolve backend root (parent of scripts/) and load .env like config/settings.py
_BACKEND_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv_file() -> None:
    env_file = _BACKEND_ROOT / ".env"
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def main() -> None:
    _load_dotenv_file()
    db_name = os.getenv("POSTGRES_DB", "rgss_db")
    host = os.getenv("POSTGRES_HOST", "127.0.0.1")
    port = int(os.getenv("POSTGRES_PORT", "5432"))
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname="postgres",
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cur.fetchone() is not None
    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"created {db_name}")
    else:
        print(f"{db_name} already exists")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
