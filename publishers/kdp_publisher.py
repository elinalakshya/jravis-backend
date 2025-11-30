# publishers/kdp_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated")


def publish_kdp_book(task):
    """
    Creates KDP book outline + interior content.
    Upload is manual since KDP API does not exist.
    """
    print("📚 Generating KDP book material...")

    try:
        prompt = """
        Write a 10-chapter non-fiction book outline.
        Include 2 pages content for Chapter 1.
        Style: simple, clear, original, non-AI detectable.
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        text = response.output_text

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        path = f"{OUTPUT_FOLDER}/kdp_book.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        print("📘 KDP book file created (manual upload required).")
        return "KDP book generated"

    except Exception as e:
        print("❌ KDP Error:", e)
        return "KDP generation failed"
      
