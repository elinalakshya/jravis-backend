import sqlite3
import os
import json
import logging

DB_PATH = os.getenv("DB_PATH", "/opt/render/project/src/data/jravis.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Products table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        payload TEXT
    )
    """)

    # Gumroad OAuth tokens
    cur.execute("""
    CREATE TABLE IF NOT EXISTS gumroad_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        access_token TEXT,
        refresh_token TEXT,
        expires_at INTEGER
    )
    """)

    conn.commit()
    conn.close()
    logging.info(f"✅ SQLite DB initialized at: {DB_PATH}")


def safe_json(data):
    if isinstance(data, str):
        return data
    return json.dumps(data)

