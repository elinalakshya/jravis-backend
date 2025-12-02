import os
import requests
import logging

logger = logging.getLogger("NewsletterPublisher")

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_LIST_ID = os.getenv("BREVO_LIST_ID")

BREVO_BASE = "https://api.brevo.com/v3"


def add_contact_to_list(email):
    """
    Add a contact to the Brevo List ID.
    If the contact already exists, Brevo will ignore duplicates safely.
    """
    url = f"{BREVO_BASE}/contacts"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    payload = {
        "email": email,
        "listIds": [int(BREVO_LIST_ID)]
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        logger.info(f"[Brevo Add Contact] {r.status_code}: {r.text}")
        return r.json()
    except Exception as e:
        logger.error(f"❌ Error adding contact to Brevo list: {e}")
        return None


def send_newsletter_email(subject, html_content):
    """
    Sends a newsletter email to the entire Brevo List ID.
    """
    url = f"{BREVO_BASE}/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    payload = {
        "sender": {
            "name": "Lakshya Global Newsletter",
            "email": "no-reply@lakshya.global"
        },
        "subject": subject,
        "htmlContent": html_content,
        "listIds": [int(BREVO_LIST_ID)]
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        logger.info(f"[Brevo Send Email] {r.status_code}: {r.text}")
        return r.json()
    except Exception as e:
        logger.error(f"❌ Error sending Brevo email: {e}")
        return None
