# publishers/course_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated")


def publish_course(task):
    """
    Generates a full online course outline + lessons.
    Manual upload required (Gumroad / Payhip / Teachable).
    """
    print("📘 Creating online course...")

    try:
        prompt = """
        Create a full online course:
        - Course title
        - 8 modules
        - 5 lessons per module
        - Assignments
        - Project at end
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        course_text = response.output_text

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        path = f"{OUTPUT_FOLDER}/course_outline.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(course_text)

        print("🎓 Course generated successfully. Manual upload needed.")
        return "Course material ready"

    except Exception as e:
        print("❌ Course Error:", e)
        return "Course generation failed"
