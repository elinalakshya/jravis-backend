# -----------------------------------------------------------
# NEWSLETTER PUBLISHER — JRAVIS Email Monetization System
# -----------------------------------------------------------

import os
import requests

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")

def send_newsletter(title: str, link: str):
    print(f"[NEWSLETTER] Sending broadcast for {title}...")

    if not BREVO_API_KEY:
        print("[NEWSLETTER] ❌ Missing API Key")
        return {"status": "error"}

    try:
        url = "https://api.brevo.com/v3/smtp/email"

        data = {
            "subject": f"🔥 New Drop: {title}",
            "htmlContent": f"<h1>{title}</h1><p>{link}</p>",
            "sender": {"name": "JRAVIS", "email": "no-reply@jravis.ai"},
            "to": [{"email": "subscriber@domain.com"}]
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "api-key": BREVO_API_KEY
        }

        r = requests.post(url, json=data, headers=headers)
        print("[NEWSLETTER] Response:", r.text)

        return {"status": "ok", "response": r.text}

    except Exception as e:
        print("[NEWSLETTER] ERROR:", e)
        return {"status": "error", "reason": str(e)}
