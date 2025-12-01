import logging
from openai import OpenAI
from publishers.course_resell_publisher import save_course_pack

logger = logging.getLogger("CourseResellEngine")
client = OpenAI()


def generate_course_pack():
    """
    AI generates:
    - Course title
    - 5 lessons
    - Course materials
    - Upload-ready description
    """
    prompt = """
    Create a full mini-course for reselling on platforms.
    Include:
    - Title
    - 5 detailed lessons
    - 2 bonus materials (PDF-style text content)
    - Course marketplace description

    Format in JSON:
    {
        "title": "...",
        "lessons": ["...", "..."],
        "materials": {
            "resource1.txt": "...",
            "resource2.txt": "..."
        },
        "description": "..."
    }
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return r.choices[0].message["content"]


def run_course_resell_engine():
    logger.info("🎓 Course Resell Engine Running...")

    try:
        import json
        data = generate_course_pack()
        parsed = json.loads(data)

        save_course_pack(
            parsed["title"],
            parsed["lessons"],
            parsed["materials"],
            parsed["description"]
        )

        logger.info("✅ Course Pack Created Successfully")

    except Exception as e:
        logger.error(f"❌ Course Engine Error: {e}")
