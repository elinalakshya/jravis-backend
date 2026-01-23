import os
from typing import Dict
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import uuid


def generate_product() -> Dict:
    title = "Morning Routine Planner – Printable Productivity Toolkit"
    description = "Morning Routine Planner designed to help users stay consistent, organized, and achieve measurable improvement. Clean printable format."
    price = 149

    os.makedirs("factory_output", exist_ok=True)

    filename = f"planner_{uuid.uuid4().hex[:8]}.pdf"
    file_path = os.path.join("factory_output", filename)

    # ---- CREATE SIMPLE PDF ----
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 80, title)

    c.setFont("Helvetica", 12)
    text = c.beginText(50, height - 130)
    for line in description.split("."):
        text.textLine(line.strip())
    c.drawText(text)

    c.showPage()
    c.save()

    print("📄 PDF CREATED:", file_path)

    return {
        "zip_path": file_path,      # still named zip_path for engine compatibility
        "name": title,
        "price": price,
        "description": description
    }

