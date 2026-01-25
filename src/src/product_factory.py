import os
import uuid
import zipfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE_DIR = "factory_output"
os.makedirs(BASE_DIR, exist_ok=True)


def _make_pdf(path, title, lines):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, y, title)

    y -= 40
    c.setFont("Helvetica", 11)

    for line in lines:
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - 60
        c.drawString(60, y, line)
        y -= 18

    c.save()


def generate_product():
    uid = uuid.uuid4().hex[:8]

    title = "Morning Routine Planner – Printable Productivity Toolkit"
    price = 149

    description = (
        "Morning Routine Planner designed to help users stay consistent,\n"
        "organized, and achieve measurable improvement.\n\n"
        "Use this planner daily:\n"
        "- Morning goals\n"
        "- Focus block\n"
        "- Reflection notes\n\n"
        "Stay consistent. Stay focused."
    )

    # -------- FILE PATHS --------
    pack_dir = os.path.join(BASE_DIR, f"pack_{uid}")
    os.makedirs(pack_dir, exist_ok=True)

    planner_pdf = os.path.join(pack_dir, "Planner.pdf")
    instructions_pdf = os.path.join(pack_dir, "Instructions.pdf")
    license_txt = os.path.join(pack_dir, "License.txt")

    zip_path = os.path.join(BASE_DIR, f"Morning_Routine_Pack_{uid}.zip")

    # -------- PLANNER PDF --------
    planner_lines = [
        "TODAY'S MORNING GOALS:",
        "• ______________________________",
        "• ______________________________",
        "",
        "FOCUS BLOCK:",
        "What is the ONE task that matters today?",
        "______________________________________",
        "",
        "REFLECTION:",
        "What went well?",
        "______________________________________",
        "",
        "What can improve tomorrow?",
        "______________________________________",
    ]

    _make_pdf(planner_pdf, "Morning Routine Planner", planner_lines)

    # -------- INSTRUCTIONS PDF --------
    instructions_lines = [
        "HOW TO USE THIS PLANNER",
        "",
        "1. Fill your top 1–3 goals each morning.",
        "2. Decide your main focus task.",
        "3. At night, reflect honestly.",
        "",
        "Use this daily for best results.",
        "",
        "Consistency beats intensity.",
    ]

    _make_pdf(instructions_pdf, "Planner Instructions", instructions_lines)

    # -------- LICENSE --------
    with open(license_txt, "w") as f:
        f.write(
            "LICENSE TERMS\n\n"
            "This product is for personal use only.\n"
            "You may not resell, redistribute, or share these files.\n\n"
            "© JRAVIS Digital Products\n"
        )

    # -------- ZIP PACK --------
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(planner_pdf, arcname="Planner.pdf")
        z.write(instructions_pdf, arcname="Instructions.pdf")
        z.write(license_txt, arcname="License.txt")

    return {
        "title": title,
        "description": description,
        "price": price,
        "zip_path": zip_path,
    }
