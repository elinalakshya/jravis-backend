import json
import random
import datetime

def run():
    """
    JRAVIS Worker — Stream 8
    Task: Affiliate SEO Blog Generator (Hybrid Automation)
    Output: JSON
    """

    # High converting affiliate niches
    niches = [
        "AI Tools",
        "Productivity Apps",
        "Make Money Online",
        "Fitness Gadgets",
        "Lifestyle Products",
        "Finance Apps",
        "Crypto Basics",
        "Business Software",
        "Marketing Automation Tools",
        "Self Improvement"
    ]

    # Blog styles
    blog_styles = [
        "Listicle",
        "Comparison",
        "Beginner Guide",
        "Step-by-Step Tutorial",
        "Top 10 Tools Style",
        "Ultimate Guide",
        "Problem-Solution",
    ]

    # AI-generated affiliate-friendly calls to action
    affiliate_ctas = [
        "Try this tool for free here →",
        "Get a special discount here →",
        "Recommended tool link →",
        "Check pricing here →",
        "Best alternative here →"
    ]

    niche = random.choice(niches)
    style = random.choice(blog_styles)

    # Generate SEO-friendly title
    title = f"{style}: {niche} in 2025"

    # Keywords for ranking
    keywords = [
        f"{niche.lower()} review",
        f"{niche.lower()} tools",
        f"best {niche.lower()} apps",
        f"{niche.lower()} guide",
        f"{niche.lower()} 2025"
    ]

    # Blog outline
    outline = [
        f"Introduction to {niche}",
        f"Why {niche} is important in 2025",
        f"Top 5 tools/products for {niche}",
        f"Pros & Cons of using these tools",
        f"How to pick the best {niche.lower()} tool",
        "Final verdict",
    ]

    # Generate intro paragraph
    intro = (
        f"{niche} is becoming one of the fastest-growing areas in 2025. "
        "In this blog, we break down everything you need to know, along with "
        "the best tools and products you can start using today."
    )

    # Generate affiliate placements
    affiliate_links = [
        {
            "tool_name": f"{niche} Tool {i+1}",
            "cta": random.choice(affiliate_ctas),
            "placeholder_link": "https://your-affiliate-link.com"
        }
        for i in range(3)
    ]

    output = {
        "stream": "affiliate_seo_blog",
        "status": "completed",
        "niche": niche,
        "style": style,
        "title": title,
        "keywords": keywords,
        "outline": outline,
        "intro_paragraph": intro,
        "affiliate_sections": affiliate_links,
        "mode": "hybrid",
        "note": (
            "JRAVIS generated full SEO blog structure. "
            "Manual Step: Expand outline into full 1200–1500 word article "
            "or let JRAVIS Brain convert outline into full blog."
        ),
        "timestamp": str(datetime.datetime.utcnow())
    }

    print(json.dumps(output, indent=4))
