import sqlite3
import os
import json
import logging

DB_PATH = os.getenv("DB_PATH", "/opt/render/project/src/data/jravis.db")

logging.basicConfig(level=logging.INFO)


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Products table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            payload TEXT,
            gumroad_id TEXT,
            gumroad_payload TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Listings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            product_id TEXT,
            payload TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    logging.info(f"✅ SQLite DB initialized at: {DB_PATH}")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


def safe_json(value):
    """
    Ensures anything stored into SQLite is JSON string, not dict/list.
    """
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return value

