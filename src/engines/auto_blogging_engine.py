import logging
import random
from openai import OpenAI
from publishers.blog_publisher import save_blog_post

logger = logging.getLogger("AutoBloggingEngine")
client = OpenAI()

CATEGORIES = {
    "AI": [
        "best ai tools", "ai income ideas", "automation hacks",
        "earn money with ai", "ai business opportunities"
    ],
    "Income": [
        "side income ideas", "freelancing tips", "online business",
        "digital product ideas", "passive income"
    ],
    "Health": [
        "health hacks", "weight loss tips", "mental wellness",
        "healthy routines", "fitness motivation"
    ],
    "Mixed": [
        "travel ideas", "lifestyle hacks", "motivation",
        "career tips", "productivity tricks"
    ]
}


def generate_blog(category, keyword):
    """AI generates a complete blog article in HTML + Markdown."""
    prompt = f"""
    Write a high-quality SEO blog article about '{keyword}'.
    Include:
    - Title
    - Intro paragraph
    - 5 subheadings with explanations
    - Conclusion with a motivational CTA

    Output 2 parts:
    1) HTML version inside <html><body> ... </body></html>
    2) Markdown version after the HTML block
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content = r.choices[0].message["content"]

    # Split HTML and Markdown
    if "</html>" in content:
        html_part = content.split("</html>")[0] + "</html>"
        md_part = content.split("</html>")[1].strip()
    else:
        html_part = content
        md_part = content

    # Extract title
    title = "Blog Article"
    if "<h1>" in html_part:
        title = html_part.split("<h1>")[1].split("</h1>")[0].strip()

    return title, html_part, md_part


def run_auto_blogging_engine():
    """Main engine to generate 5–20 articles per run."""
    logger.info("📝 Auto Blogging Engine Running...")

    try:
        # Generate between 5 to 20 articles each cycle
        count = random.randint(5, 20)

        for _ in range(count):
            category = random.choice(list(CATEGORIES.keys()))
            keyword = random.choice(CATEGORIES[category])

            title, html, md = generate_blog(category, keyword)
            save_blog_post(category, title, html, md)

        logger.info("✅ Auto Blogging Cycle Completed")

    except Exception as e:
        logger.error(f"❌ Auto Blogging Engine Error: {e}")
