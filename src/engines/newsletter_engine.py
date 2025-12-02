import logging
import time
from openai import OpenAI
from publishers.newsletter_publisher import send_newsletter_email

logger = logging.getLogger("NewsletterEngine")
client = OpenAI()


def generate_daily_newsletter():
    """AI-generated short daily newsletter."""
    prompt = """
    Write a short, powerful daily newsletter for 'Lakshya Global Newsletter'.
    Include:
    - 1 motivational line
    - 1 actionable income or productivity tip
    - 1 short trending AI or business update
    Keep it under 150 words.
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message["content"]


def generate_weekly_digest():
    """AI-generated long weekly summary newsletter."""
    prompt = """
    Write a detailed weekly digest for 'Lakshya Global Newsletter'.
    Include:
    - Summary of the week's opportunities
    - 3 income/growth hacks
    - 2 automation insights
    - 1 inspirational closing message
    Length: 400–600 words.
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message["content"]


def run_newsletter_engine():
    """Automatically handles daily + weekly sending schedule."""
    logger.info("🟦 Newsletter Engine Checking...")

    now = time.localtime()
    hour = now.tm_hour
    weekday = now.tm_wday  # Monday=0, Sunday=6

    try:
        # DAILY NEWSLETTER — 10 AM IST
        if hour == 10:
            logger.info("📨 Sending DAILY Newsletter...")
            content = generate_daily_newsletter()
            send_newsletter_email(
                "🌅 Lakshya Daily Boost",
                f"<html><body>{content}</body></html>"
            )

        # WEEKLY DIGEST — Sunday 11 AM IST
        if weekday == 6 and hour == 11:
            logger.info("📨 Sending WEEKLY Digest...")
            content = generate_weekly_digest()
            send_newsletter_email(
                "📘 Lakshya Weekly Digest",
                f"<html><body>{content}</body></html>"
            )

    except Exception as e:
        logger.error(f"❌ Newsletter Engine Error: {e}")
