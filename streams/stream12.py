import json
import random
import datetime

def run():
    """
    JRAVIS Worker — Stream 12
    Task: Micro-Niche Affiliate Website Content (Hybrid Automation)
    Output: JSON
    """

    # Micro-niche ideas (fast earning potential)
    niches = [
        "AI Tools for Students",
        "Healthy Meal Prep for Busy Professionals",
        "Travel Gear for Solo Travelers",
        "Pet Accessories for Small Dogs",
        "Budget Gadgets for Programmers",
        "Home Gym Equipment for Beginners",
        "Eco-Friendly Kitchen Products",
        "Productivity Tools for Remote Workers",
        "Affordable Tech for Students",
        "Digital Planners for Women"
    ]

    # Page types JRAVIS should create
    page_types = [
        "Top 5 Picks",
        "Best Products Guide",
        "Comparison Review",
        "Beginner Buying Guide",
        "Ultimate FAQ Page",
        "How-To Article",
        "Listicle"
    ]

    # Affiliate CTA templates
    affiliate_ctas = [
        "Check price on Amazon →",
        "See the discounted deal →",
        "Best value option →",
        "Buy now on the official website →",
        "See more customer reviews →"
    ]

    niche = random.choice(niches)
    page_type = random.choice(page_types)

    # SEO-friendly title
    title = f"{page_type}: {niche} (2025 Guide)"

    # Generate keywords
    keywords = [
        niche.lower(),
        f"{niche.lower()} review",
        f"{niche.lower()} top picks",
        f"best {niche.lower()}",
        f"{niche.lower()} amazon",
    ]

    # Generate 5 affiliate product sections
    num_products = 5
    products = []

    for i in range(num_products):
        product_name = f"{niche.split()[0]} Product {i+1}"
        products.append({
            "name": product_name,
            "summary": f"A high-value product for {niche.lower()} users.",
            "pros": [
                "Affordable", 
                "High customer rating", 
                "Beginner friendly"
            ],
            "cons": [
                "Limited color options",
                "Sometimes out of stock"
            ],
            "affiliate_cta": random.choice(affiliate_ctas),
            "affiliate_link": "https://your-amazon-affiliate-link.com"
        })

    # Intro paragraph
    intro = (
        f"Welcome to the ultimate guide on {niche.lower()}. "
        f"This {page_type.lower()} helps you choose the best products quickly "
        "with clear pros, cons, summaries, and affiliate links."
    )

    # FAQ structure
    faq = [
        {
            "question": f"What is the best product for {niche.lower()}?",
            "answer": f"It depends on your needs, but Product 1 is a great starting point."
        },
        {
            "question": f"Is {niche.lower()} expensive?",
            "answer": "Most products are budget-friendly and beginner-safe."
        },
        {
            "question": f"How do I choose {niche.lower()} products?",
            "answer": "Look for customer reviews, features, and your personal needs."
        }
    ]

    output = {
        "stream": "micro_niche_affiliate_sites",
        "status": "completed",
        "niche": niche,
        "page_type": page_type,
        "title": title,
        "intro_paragraph": intro,
        "keywords": keywords,
        "products": products,
        "faq": faq,
        "mode": "hybrid",
        "note": (
            "JRAVIS generated micro-niche website content. "
            "Manual Step: Convert JSON → blog pages on your micro-niche website "
            "and insert Amazon affiliate links."
        ),
        "timestamp": str(datetime.datetime.utcnow())
    }

    print(json.dumps(output, indent=4))
