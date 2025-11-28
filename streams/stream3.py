import json
import random
import datetime

def run():
    """
    JRAVIS Worker — Stream 3
    Task: Creative Market Digital Templates (Hybrid Automation)
    Output: JSON
    """

    # Categories that sell extremely well on Creative Market
    categories = [
        "Canva Template Pack",
        "Instagram Post Templates",
        "Business Card Templates",
        "Wedding Invitation Bundle",
        "Resume/CV Templates",
        "Branding Kit",
        "Poster Layout Bundle",
        "Ebook/Workbook Template",
        "Minimal Social Media Pack",
        "Stationery Bundle",
    ]

    # Design styles that sell well
    styles = [
        "minimal",
        "aesthetic",
        "pastel",
        "bold typography",
        "retro vintage",
        "modern clean",
        "black & gold luxury",
        "cute & playful",
        "abstract gradient",
        "neutral beige palette",
    ]

    # JRAVIS generates 4–8 digital products per run
    num_items = random.randint(4, 8)

    items = []

    for i in range(num_items):
        category = random.choice(categories)
        style = random.choice(styles)

        title = f"{style.title()} {category}"
        desc = (
            f"A {style} themed {category} created for designers, entrepreneurs, "
            "and social media managers. Fully editable and easy to customize."
        )

        item = {
            "id": f"creative_market_item_{i+1}",
            "category": category,
            "style": style,
            "title": title,
            "description": desc,
            "contents": [
                "Editable files (PDF/Canva/PSD)",
                "Font recommendations",
                "Brand color palette",
                "Mockup preview images"
            ],
            "tags": [
                "template", "branding", "digital-product",
                style.replace(" ", "-"), category.replace(" ", "-").lower()
            ],
            "bundle_suggestion": random.choice([
                "Combine with social media pack",
                "Add matching business card design",
                "Create deluxe branding kit upgrade",
                "Pair with resume templates for extra sales"
            ]),
            "created_at": str(datetime.datetime.utcnow())
        }

        items.append(item)

    output = {
        "stream": "creative_market",
        "status": "completed",
        "total_products": num_items,
        "items": items,
        "mode": "hybrid",
        "note": (
            "JRAVIS generated the full product specs. "
            "Manual step: Use Canva/Photoshop to create the actual files, "
            "then upload to Creative Market."
        ),
        "timestamp": str(datetime.datetime.utcnow())
    }

    print(json.dumps(output, indent=4))
