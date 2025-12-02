# publishers/micro_niche_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated")


def publish_micro_niche_site(task):
    """
    Creates micro niche website content for affiliate pages.
    """
    print("🌐 Creating micro niche site page...")

    try:
        prompt = """
        Generate a full micro-niche website homepage with:
        - SEO title
        - H1 headline
        - 3 affiliate products (review style)
        - Pros and cons
        - FAQ
        - CTA
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        page = response.output_text

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        path = f"{OUTPUT_FOLDER}/micro_niche_homepage.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(page)

        print("🌎 Micro niche site content ready.")
        return "Micro niche content generated"

    except Exception as e:
        print("❌ Micro Niche Error:", e)
        return "Micro niche generation failed"
