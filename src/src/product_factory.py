import os
import uuid

<<<<<<< HEAD
<<<<<<< HEAD

OUTPUT_DIR = "factory_output"
=======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "factory_output")
>>>>>>> 1f57279cb1e2a7d049ea5ef7a4b8c6cf7fd106fa
=======
OUTPUT_DIR = "factory_output"
>>>>>>> 841ae53c3b0e30b8e1e18baaa1e1dd945f7b46c0
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_product():
<<<<<<< HEAD
<<<<<<< HEAD
    """
    Generates a simple TXT product for now.
    Later we will switch to PDF packs + ZIP.
    """

    product_id = uuid.uuid4().hex[:8]

=======
>>>>>>> 1f57279cb1e2a7d049ea5ef7a4b8c6cf7fd106fa
    title = "Morning Routine Planner – Printable Productivity Toolkit"
=======
    uid = uuid.uuid4().hex[:8]
>>>>>>> 841ae53c3b0e30b8e1e18baaa1e1dd945f7b46c0

    title = "Morning Routine Planner – Printable Productivity Toolkit"
    description = (
        "Morning Routine Planner designed to help users stay consistent,\n"
        "organized, and achieve measurable improvement.\n\n"
        "Use this planner daily:\n"
        "- Morning goals\n"
        "- Focus block\n"
        "- Reflection notes\n\n"
        "Stay consistent. Stay focused."
    )
    price = 149

<<<<<<< HEAD
<<<<<<< HEAD
    file_name = f"planner_{product_id}.txt"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    content = f"""
{title}

-----------------------

{description}

-----------------------

Daily Sections:

1. Top Priority
2. Focus Task
3. Reflection
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
=======
    uid = uuid.uuid4().hex[:8]
    pdf_name = f"planner_{uid}.pdf"
    zip_name = f"planner_pack_{uid}.zip"

    pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
    zip_path = os.path.join(OUTPUT_DIR, zip_name)

    # ---------- CREATE PDF ----------
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)

    y -= 40
    c.setFont("Helvetica", 11)
    for line in description.split("\n"):
        c.drawString(50, y, line)
        y -= 16

    c.showPage()
    c.save()

    # ---------- CREATE ZIP ----------
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(pdf_path, arcname=pdf_name)
>>>>>>> 1f57279cb1e2a7d049ea5ef7a4b8c6cf7fd106fa
=======
    filename = f"planner_{uid}.txt"
    file_path = os.path.join(OUTPUT_DIR, filename)

    with open(file_path, "w") as f:
        f.write(title + "\n\n" + description)
>>>>>>> 841ae53c3b0e30b8e1e18baaa1e1dd945f7b46c0

    print("📄 TXT PRODUCT CREATED:", file_path)

<<<<<<< HEAD
<<<<<<< HEAD
    return {
        "file_path": file_path,
        "title": title,
        "description": description,
        "price": price,
    }

=======
>>>>>>> 1f57279cb1e2a7d049ea5ef7a4b8c6cf7fd106fa
=======
    return {
        "title": title,
        "description": description,
        "price": price,
        "file_path": file_path,
    }
>>>>>>> 841ae53c3b0e30b8e1e18baaa1e1dd945f7b46c0
