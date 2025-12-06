import os
import requests
from openai import OpenAI

BERVO_API_KEY = os.getenv("BERVO_API_KEY")
NEWSLETTER_ID = os.getenv("NEWSLETTER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_email_content(title, product_url):
    """
    Uses OpenAI to generate unique, human-like email content.
    """

    prompt = f"""
    Write a high-converting email promoting a new digital template called "{title}".
    Keep it short, warm, engaging. Avoid AI detection patterns.
    Include the product link: {product_url}.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative email copywriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        email_text = completion.choices[0].message.content
        return email_text

    except Exception as e:
        return f"Error generating content: {e}"


def send_newsletter(subject, content):
    """
    Sends email via Bervo API.
    """

    if not Bervo_API_KEY or not NEWSLETTER_ID:
        return {"status": "error", "message": "Missing Bervo credentials"}

    try:
        payload = {
            "subject": subject,
            "content": content,
            "list_id": NEWSLETTER_ID
        }

        headers = {
            "Authorization": f"Bearer {BERVO_API_KEY}",
            "Content-Type": "application/json"
        }

        res = requests.post(
            "https://api.bervo.com/v1/emails/send",
            json=payload,
            headers=headers
        ).json()

        if "error" in res:
            return {"status": "error", "message": res["error"]}

        return {"status": "success", "details": res}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def process_newsletter(title, product_url):
    """
    End-to-end pipeline:
    1. Generate AI content
    2. Send via Bervo
    """

    content = generate_email_content(title, product_url)

    result = send_newsletter(
        subject=f"New Template: {title}",
        content=content
    )

    return result
