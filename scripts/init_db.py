"""
Initialize SQLite DB from schema + seed data.
Creates rental_app.db in repo root.
"""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "rental_app.db"
SCHEMA = ROOT / "data" / "rental_app_schema.sql"
SEED   = ROOT / "data" / "seed_data.sql"

def run_sql_file(conn, path: Path):
    with open(path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH.as_posix())
    try:
        run_sql_file(conn, SCHEMA)
        run_sql_file(conn, SEED)
        conn.commit()
        print(f"✅ Created DB at {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
