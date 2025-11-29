from email_utils import send_report_email

summary_file = "test_summary.pdf"
invoice_file = "test_invoice.pdf"

with open(summary_file, "wb") as f:
    f.write(b"%PDF-1.4 test summary")

with open(invoice_file, "wb") as f:
    f.write(b"%PDF-1.4 test invoice")

send_report_email(summary_file, invoice_file, "TEST-APPROVAL-123")

print("✔ Test email sent.")
