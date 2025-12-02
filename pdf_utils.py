from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter

def generate_summary_pdf(path, data):
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "JRAVIS DAILY SUMMARY REPORT")
    c.setFont("Helvetica", 12)

    y = 760
    for line in data:
        c.drawString(50, y, f"- {line}")
        y -= 20
    
    c.save()


def generate_invoice_pdf(path, invoices):
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "JRAVIS DAILY INVOICES")
    c.setFont("Helvetica", 12)

    y = 760
    for inv in invoices:
        c.drawString(50, y, f"- {inv}")
        y -= 20

    c.save()


def encrypt_pdf(input_path, output_path, password):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(output_path, "wb") as f:
        writer.write(f)
