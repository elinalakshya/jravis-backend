# publishers/printify_publisher.py

import os
import json
from settings import PRINTIFY_API_KEY, OUTPUT_FOLDER, SAFE_OUTPUT
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def publish_printify_product(task):
    """
    Simulated Printify publisher — generates mock POD design
    and prepares data for manual upload to Printify.
    """

    print("🖨 Publishing Printify POD item...")

    try:
        # Generate placeholder design description
        ai = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate a simple POD product design concept."},
                {"role": "user", "content": "Create a minimal Printify product idea."}
            ]
        )

        description = ai.choices[0].message["content"]

        # Prepare output
        design_file = os.path.join(OUTPUT_FOLDER or SAFE_OUTPUT, "printify_design.txt")
        os.makedirs(os.path.dirname(design_file), exist_ok=True)

        with open(design_file, "w") as f:
            f.write(description)

        print("✔ Printify ready for manual review.")
        return {"status": "ok", "output": design_file}

    except Exception as e:
        print("❌ Printify Error:", str(e))
        return {"status": "error", "error": str(e)}
