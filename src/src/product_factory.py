import os
import uuid
import zipfile
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

OUTPUT_DIR = "factory_output"


def _base_doc(path):
    return SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )


def _title(text):
    styles = getSampleStyleSheet()
    styles["Title"].alignment = TA_CENTER
    return Paragraph(f"<b>{text}</b>", styles["Title"])


def _section(text):
    styles = getSampleStyleSheet()
    return Paragraph(f"<b>{text}</b>", styles["Heading3"])


def _blank_table(rows, cols, height=30):
    data = [["" for _ in range(cols)] for _ in range(rows)]
    t = Table(data, colWidths="*", rowHeights=height)
    t.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
            ]
        )
    )
    return t


# -----------------------------
# INDIVIDUAL WORKSHEETS
# -----------------------------

def build_cover(path, title):
    doc = _base_doc(path)
    story = []
    story.append(Spacer(1, 200))
    story.append(_title(title))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Printable Productivity Toolkit", getSampleStyleSheet()["BodyText"]))
    story.append(Spacer(1, 200))
    story.append(Paragraph("© Team Lakshya", getSampleStyleSheet()["BodyText"]))
    doc.build(story)


def build_daily(path):
    doc = _base_doc(path)
    s = []
    s.append(_title("Daily Planner"))
    s.append(Spacer(1, 10))

    s.append(_section("Top 3 Priorities"))
    s.append(_blank_table(4, 1, 35))
    s.append(Spacer(1, 10))

    s.append(_section("Schedule"))
    s.append(_blank_table(10, 2, 28))
    s.append(Spacer(1, 10))

    s.append(_section("Notes"))
    s.append(_blank_table(6, 1, 35))

    doc.build(s)


def build_weekly(path):
    doc = _base_doc(path)
    s = []
    s.append(_title("Weekly Planner"))
    s.append(Spacer(1, 10))

    s.append(_blank_table(8, 3, 35))
    s.append(PageBreak())
    s.append(_section("Weekly Goals"))
    s.append(_blank_table(6, 1, 35))

    doc.build(s)


def build_habits(path):
    doc = _base_doc(path)
    s = []
    s.append(_title("Habit Tracker"))
    s.append(Spacer(1, 10))

    table = [["Habit", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]]
    for _ in range(10):
        table.append([""] * 8)

    t = Table(table, colWidths="*", rowHeights=30)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.8, colors.black)]))
    s.append(t)

    doc.build(s)


def build_reflection(path):
    doc = _base_doc(path)
    s = []
    s.append(_title("Reflection Journal"))
    s.append(Spacer(1, 10))

    s.append(_section("What went well?"))
    s.append(_blank_table(6, 1, 30))
    s.append(Spacer(1, 10))

    s.append(_section("What can improve?"))
    s.append(_blank_table(6, 1, 30))
    s.append(Spacer(1, 10))

    s.append(_section("Tomorrow's Focus"))
    s.append(_blank_table(4, 1, 30))

    doc.build(s)


# -----------------------------
# MAIN FACTORY
# -----------------------------

def generate_product():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    product_id = uuid.uuid4().hex[:8]
    title = "Morning Routine Planner – Printable Productivity Toolkit"

    pack_dir = os.path.join(OUTPUT_DIR, f"pack_{product_id}")
    os.makedirs(pack_dir, exist_ok=True)

    cover = os.path.join(pack_dir, "01_Cover.pdf")
    daily = os.path.join(pack_dir, "02_Daily_Planner.pdf")
    weekly = os.path.join(pack_dir, "03_Weekly_Planner.pdf")
    habit = os.path.join(pack_dir, "04_Habit_Tracker.pdf")
    reflect = os.path.join(pack_dir, "05_Reflection_Journal.pdf")

    build_cover(cover, title)
    build_daily(daily)
    build_weekly(weekly)
    build_habits(habit)
    build_reflection(reflect)

    zip_name = f"Morning_Routine_Pack_{product_id}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in [cover, daily, weekly, habit, reflect]:
            z.write(f, arcname=os.path.basename(f))

    # cleanup loose pdfs
    for f in [cover, daily, weekly, habit, reflect]:
        os.remove(f)
    os.rmdir(pack_dir)

    return {
        "title": title,
        "zip_path": zip_path,
        "price": 149,
    }
