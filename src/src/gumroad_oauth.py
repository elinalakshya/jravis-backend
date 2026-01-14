# src/src/gumroad_oauth.py

import os
import requests
import sqlite3
import logging
from urllib.parse import urlencode

GUMROAD_CLIENT_ID = os.getenv("GUMROAD_CLIENT_ID")
GUMROAD_CLIENT_SECRET = os.getenv("GUMROAD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GUMROAD_REDIRECT_URI")

AUTH_URL = "https://gumroad.com/oauth/authorize"
TOKEN_URL = "https://api.gumroad.com/oauth/token"

DB_PATH = "/opt/render/project/src/data/jravis.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def get_auth_url():
    params = {
        "client_id": GUMROAD_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "view_profile edit_products"
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str):
    data = {
        "client_id": GUMROAD_CLIENT_ID,
        "client_secret": GUMROAD_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    r = requests.post(TOKEN_URL, data=data, timeout=30)

    if r.status_code != 200:
        raise Exception(f"Token exchange failed: {r.text}")

    return r.json()


def save_tokens(token_data: dict):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS gumroad_tokens (
            id INTEGER PRIMARY KEY,
            access_token TEXT,
            refresh_token TEXT
        )
    """)

    cur.execute("DELETE FROM gumroad_tokens")

    cur.execute(
        "INSERT INTO gumroad_tokens (access_token, refresh_token) VALUES (?, ?)",
        (token_data.get("access_token"), token_data.get("refresh_token"))
    )

    conn.commit()
    conn.close()


def get_access_token():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT access_token FROM gumroad_tokens LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return row[0]
