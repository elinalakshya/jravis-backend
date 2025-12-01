import logging
from openai import OpenAI
from publishers.template_machine_publisher import save_template_pack

logger = logging.getLogger("TemplateMachineEngine")
client = OpenAI()

def generate_template_pack():
    """
    Generate a full template pack in JSON:
    - Title
    - 3–5 templates (filename : content)
    """
    prompt = """
    Create a pack of useful digital templates.
    Include:
    - A short title
    - 4 templates (business, notion, planner, resume)
    Format as:
    {
        "title": "...",
        "files": {
            "business_template.txt": "...",
            "notion_template.txt": "...",
            "planner.txt": "...",
            "resume_template.txt": "..."
        }
    }
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return r.choices[0].message["content"]


def run_template_machine_engine():
    logger.info("📝 Template Machine Engine Running...")

    try:
        import json
        data = json.loads(generate_template_pack())

        save_template_pack(
            data["title"],
            data["files"]
        )

        logger.info("✅ Template Machine Pack Generated")

    except Exception as e:
        logger.error(f"❌ Template Machine Engine Error: {e}")
