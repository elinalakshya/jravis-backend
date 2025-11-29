import smtplib
import ssl
from email.message import EmailMessage
from settings import EMAIL_USER, EMAIL_PASS

# Always send to Boss
EMAIL_TO = "nrveeresh327@gmail.com"


def send_report_email(summary_pdf_path, invoice_pdf_path, approval_token):
    msg = EmailMessage()
    msg["Subject"] = "JRAVIS Daily Report – Approval Needed"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    msg.set_content(
        f"""
Hello Boss,

Your JRAVIS automated daily report is ready.

Attached:
1. Locked Summary Report (requires code)
2. Invoice Report

Approval Token: {approval_token}

Please approve within 10 minutes to continue automation.

– JRAVIS Automation System
"""
    )

    # Attach Summary PDF
    with open(summary_pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="summary_locked.pdf"
        )

    # Attach Invoice PDF
    with open(invoice_pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="invoice.pdf"
        )

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print(f"📤 Email sent successfully to: {EMAIL_TO}")
