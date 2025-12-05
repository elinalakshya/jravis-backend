import os

OUTPUT_DIR = "output/payhip"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_payhip_product(title: str, html: str):
    """Save Payhip product HTML."""
    safe_title = title.replace(" ", "_").replace("/", "_")
    filepath = os.path.join(OUTPUT_DIR, f"{safe_title}.html")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath
