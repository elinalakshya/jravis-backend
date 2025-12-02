# Creative Market Publisher (Mock flow)
# Creative Market does NOT provide a real upload API.
# So JRAVIS will generate the digital asset + prepare ZIP + return info.

import os
import json
import uuid
from settings import OUTPUT_FOLDER, SAFE_OUTPUT
from openai import OpenAI

client = OpenAI()

def publish_creative_market_item(task):
    """
    Generates a digital template bundle and prepares it for manual upload.
    JRAVIS cannot auto-upload to Creative Market (API unavailable).
    """

    print("🎨 Preparing Creative Market template bundle...")

    # Generate template description
    prompt = "Generate a premium design template description for Creative Market."
    response = client.responses.create(model="gpt-4o-mini", input=prompt)

    description = response.output_text or "Premium design asset for Creative Market."

    # Safe output folder
    out_dir = SAFE_OUTPUT("creative_market")
    os.makedirs(out_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    asset_path = os.path.join(out_dir, f"creative_template_{file_id}.txt")

    # Save result
    with open(asset_path, "w") as f:
        f.write(description)

    result = {
        "status": "ready_for_manual_upload",
        "asset_file": asset_path,
        "message": "Creative Market does not support automatic uploads. File is prepared."
    }

    print("✨ Creative Market bundle generated.")
    print(f"📦 Saved at: {asset_path}")
    return result
