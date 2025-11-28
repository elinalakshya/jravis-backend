import json
import random
import datetime

def run():
    """
    JRAVIS Worker — Stream 7
    Task: Shopify Digital Products (Hybrid Automation)
    Output: JSON
    """

    # Digital product types that sell extremely well
    product_types = [
        "Digital Planner",
        "Ebook Guide",
        "Business Worksheet Pack",
        "Branding Kit",
        "Marketing Template Bundle",
        "Meal Planner & Fitness Tracker",
        "Daily Productivity Journal",
        "Study Notes (Academic Subject)",
        "Content Calendar Template",
        "Printable Habit Tracker",
    ]

    # Design styles
    styles = [
        "minimal aesthetic",
        "pastel modern",
        "neutral beige",
        "bold typography",
        "cute kawaii",
        "gradient abstract",
        "retro vintage",
        "professional business blue"
    ]

    # Generate 4–7 digital products
    num_products = random.randint(4, 7)

    products = []

    for i in range(num_products):
        product_type = random.choice(product_types)
        style = random.choice(styles)

        title = f"{style.title()} {product_type}"
        description = (
            f"A beautifully designed {product_type} in {style} style. "
            "Fully printable and easy to use. Ideal for digital planners, "
            "entrepreneurs, students, and productivity lovers."
        )

        # Inside the product
        content_structure = [
            "PDF version",
            "Editable Canva template link",
            "Brand color palette",
            "Typography guide",
            "Bonus pages (if applicable)"
        ]

        # SEO Tags
        tags = [
            "digital-product",
            "printable",
            "shopify",
            product_type.replace(" ", "-").lower(),
            style.replace(" ", "-")
        ]

        products.append({
            "id": f"shopify_product_{i+1}",
            "product_type": product_type,
            "style": style,
            "title": title,
            "description": description,
            "contents": content_structure,
            "tags": tags,
            "bundle_idea": random.choice([
                "Combine with a matching worksheet pack",
                "Add as part of a productivity mega bundle",
                "Offer as a monthly update subscription"
            ]),
            "created_at": str(datetime.datetime.utcnow())
        })

    output = {
        "stream": "shopify_digital_products",
        "status": "completed",
        "total_products": num_products,
        "products_created": products,
        "mode": "hybrid",
        "note": (
            "JRAVIS generated product content. "
            "Manual Step: Create final PDF/Canva templates and upload to Shopify."
        ),
        "timestamp": str(datetime.datetime.utcnow())
    }

    print(json.dumps(output, indent=4))
