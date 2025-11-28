import smtplib
import ssl
from email.message import EmailMessage
from settings import EMAIL_USER, EMAIL_PASS, BACKEND_URL

def send_report_email(summary_path, invoice_path, token):
    msg = EmailMessage()
    msg["Subject"] = "JRAVIS Daily Report — Approval Required"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    approval_url = f"{BACKEND_URL}/report/approve/{token}"

    body = f"""
Boss,

Your JRAVIS daily report is ready.

Summary PDF is encrypted with your lock code.
Invoice PDF is attached separately.

Click to approve JRAVIS to continue today’s work:
{approval_url}

If not approved in 10 minutes, JRAVIS auto-resumes.

– JRAVIS (Mission 2040)
"""
    msg.set_content(body)

    # Attach Summary PDF
    with open(summary_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf",
                           filename="summary_locked.pdf")

    # Attach Invoice PDF
    with open(invoice_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf",
                           filename="invoice.pdf")

    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
