import time

def send_newsletter(title):
    print(f"[NEWSLETTER] Sending broadcast for {title}...")

    time.sleep(1)

    return {
        "status": "sent",
        "platform": "newsletter",
        "subject": f"New Template: {title}"
    }
