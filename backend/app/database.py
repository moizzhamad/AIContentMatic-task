"""
Database access and helper utilities for SQLite.
"""

import os
import shutil
import sqlite3
from typing import Generator

# Database path in data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find_source_db_path() -> str:
    candidates = [
        os.path.join(BASE_DIR, "data", "market_data.db"),
        os.path.join(BACKEND_DIR, "data", "market_data.db"),
        os.path.join(os.getcwd(), "data", "market_data.db"),
        os.path.join(os.getcwd(), "backend", "data", "market_data.db"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]

SOURCE_DB_PATH = find_source_db_path()

def get_effective_db_path() -> str:
    """Returns DB path, copying to /tmp in serverless (e.g. Vercel) read-only environments."""
    effective_src = find_source_db_path()
    if os.environ.get("VERCEL") or not os.access(os.path.dirname(effective_src), os.W_OK):
        tmp_dir = "/tmp"
        tmp_db = os.path.join(tmp_dir, "market_data.db")
        if not os.path.exists(tmp_db):
            if os.path.exists(effective_src):
                shutil.copyfile(effective_src, tmp_db)
            else:
                try:
                    from data.generate_market_data import generate_market_data
                    generate_market_data()
                except Exception:
                    pass
                if os.path.exists(effective_src):
                    shutil.copyfile(effective_src, tmp_db)
        return tmp_db
    return effective_src

def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with Row row_factory for dict-like access."""
    db_path = get_effective_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def reset_user_simulation():
    """Resets user account to $100,000 and clears all holdings and transactions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM portfolio_positions")
    cursor.execute("UPDATE user_account SET cash_balance = initial_balance WHERE id = 1")
    conn.commit()
    conn.close()
