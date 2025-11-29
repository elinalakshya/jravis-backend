import smtplib
from email.message import EmailMessage

from settings import (
    SMTP_HOST,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASS
)

BOSS_EMAIL = "nrveeresh327@gmail.com"   # <--- FIXED


def send_report_email(locked_summary, invoice, approval_token):
    msg = EmailMessage()
    msg['Subject'] = f"JRAVIS Daily Report – Approval Needed ({approval_token})"
    msg['From'] = EMAIL_USER
    msg['To'] = BOSS_EMAIL

    msg.set_content(
        f"""
Hello Boss,

Your JRAVIS daily report is ready.

Approval Token: {approval_token}

Two files attached:
1. Locked Summary (password protected)
2. Invoice (no password)

Regards,
JRAVIS Automated Worker
        """
    )

    # Attach Summary
    with open(locked_summary, "rb") as f:
        msg.add_attachment(f.read(), maintype="application",
                           subtype="pdf", filename="summary_locked.pdf")

    # Attach Invoice
    with open(invoice, "rb") as f:
        msg.add_attachment(f.read(), maintype="application",
                           subtype="pdf", filename="invoice.pdf")

    # Send Email
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.sendmail(EMAIL_USER, BOSS_EMAIL, msg.as_string())

    print("✔ Email sent to Boss:", BOSS_EMAIL)
