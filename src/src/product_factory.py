import os, uuid, zipfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(path, title):
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, title)
    c.drawString(50, 770, "Daily Planner Page")
    c.showPage()
    c.save()


def generate_product(niche="general"):
    os.makedirs("factory_output", exist_ok=True)

    uid = uuid.uuid4().hex[:8]
    title = "Morning Routine Planner – Printable Productivity Toolkit"

    pdf_files = []
    for i in range(1, 4):
        pdf = f"factory_output/{niche}_page_{uid}_{i}.pdf"
        generate_pdf(pdf, f"{title} – {niche.capitalize()} Page {i}")
        pdf_files.append(pdf)

    zip_name = f"factory_output/Morning_Routine_Pack_{uid}.zip"
    with zipfile.ZipFile(zip_name, "w") as z:
        for p in pdf_files:
            z.write(p, arcname=os.path.basename(p))

    return {
        "title": title,
        "niche": niche,
        "zip_path": zip_name
    }
