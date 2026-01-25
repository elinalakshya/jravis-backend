import os
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

OUTPUT_DIR = "factory_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _wrap_text(text, max_chars=90):
    words = text.split()
    lines = []
    line = ""

    for w in words:
        if len(line) + len(w) + 1 <= max_chars:
            line += (" " if line else "") + w
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)

    return lines


def generate_product():
    title = "Morning Routine Planner – Printable Productivity Toolkit"

    description = (
        "Use this planner daily to stay focused and consistent.\n\n"
        "Sections included:\n"
        "- Morning goals\n"
        "- Focus block\n"
        "- Reflection notes\n\n"
        "Stay consistent. Stay focused."
    )

    price = 149

    uid = uuid.uuid4().hex[:8]
    pdf_path = os.path.join(OUTPUT_DIR, f"planner_{uid}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # ------------------------
    # PAGE 1 — COVER
    # ------------------------
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 80, title)

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 130, "Printable Productivity Toolkit")

    c.showPage()

    # ------------------------
    # PAGE 2 — PLANNER CONTENT
    # ------------------------
    y = height - 40
    c.setFont("Helvetica", 12)

    sections = [
        "Morning Goals",
        "",
        "__________________________________________",
        "",
        "__________________________________________",
        "",
        "Focus Block",
        "",
        "__________________________________________",
        "",
        "__________________________________________",
        "",
        "Reflection Notes",
        "",
        "__________________________________________",
        "",
        "__________________________________________",
        "",
    ]

    for line in sections:
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 40

        c.drawString(40, y, line)
        y -= 18

    c.save()

    print("📄 PDF PRODUCT CREATED:", pdf_path)

    return {
        "title": title,
        "description": description,
        "price": price,
        "file_path": pdf_path,
    }
