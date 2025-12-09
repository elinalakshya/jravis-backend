from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify

def run_publishers(title, zip_path, logger=print):
    logger("📤 Publishing product...")

    # Content
    description = f"Automated JRAVIS Template: {title}"

    # Gumroad
    try:
        r = publish_to_gumroad(title, description, zip_path)
        logger("→ Gumroad:", r)
    except Exception as e:
        logger("❌ Gumroad error:", e)

    # Payhip
    try:
        r = publish_to_payhip(title, description, zip_path)
        logger("→ Payhip:", r)
    except Exception as e:
        logger("❌ Payhip error:", e)

    # Printify
    try:
        r = publish_to_printify(title, description)
        logger("→ Printify:", r)
    except Exception as e:
        logger("❌ Printify error:", e)

    logger("✅ Publishing complete.")
