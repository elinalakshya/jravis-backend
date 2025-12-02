from reportlab.pdfgen import canvas
from email_utils import send_report_email

# Create valid summary PDF
summary_file = "test_summary.pdf"
c = canvas.Canvas(summary_file)
c.drawString(100, 750, "JRAVIS Summary Test PDF")
c.save()

# Create valid invoice PDF
invoice_file = "test_invoice.pdf"
c2 = canvas.Canvas(invoice_file)
c2.drawString(100, 750, "JRAVIS Invoice Test PDF")
c2.save()

# Send email
send_report_email(summary_file, invoice_file, "TEST-APPROVAL-123")

print("✔ Valid test email sent with proper PDFs.")
