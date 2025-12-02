import logging
from openai import OpenAI
from publishers.newsletter_content_publisher import save_newsletter_issue

logger = logging.getLogger("NewsletterContentEngine")
client = OpenAI()


def generate_newsletter_issue():
    """AI generates a monetized newsletter issue."""
    prompt = """
    Create a full newsletter issue about AI, automation, business, or productivity.
    Include:
    - Title (H1)
    - Strong intro
    - 3 major sections
    - One sponsored section placeholder (SPONSOR_LINK)
    - 2 affiliate recommendation spots (AFFILIATE_LINK)
    - Conclusion + CTA

    Output:
    1) HTML formatted version
    2) Markdown version
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content = r.choices[0].message["content"]

    # Separate HTML & Markdown
    if "</html>" in content:
        html = content.split("</html>")[0] + "</html>"
        md = content.split("</html>")[1].strip()
    else:
        html = content
        md = content

    # Extract title
    title = "Newsletter_Issue"
    if "<h1>" in html:
        title = html.split("<h1>")[1].split("</h1>")[0].strip()

    # Replace placeholders
    html = html.replace("AFFILIATE_LINK", "https://your-affiliate-link.com")
    md = md.replace("AFFILIATE_LINK", "https://your-affiliate-link.com")

    html = html.replace("SPONSOR_LINK", "https://your-sponsor-link.com")
    md = md.replace("SPONSOR_LINK", "https://your-sponsor-link.com")

    return title, html, md


def run_newsletter_content_engine():
    logger.info("📰 Newsletter Content Engine Running...")

    try:
        title, html, md = generate_newsletter_issue()
        save_newsletter_issue(title, html, md)

        logger.info("✅ Newsletter Issue Generated")

    except Exception as e:
        logger.error(f"❌ Newsletter Content Engine Error: {e}")
