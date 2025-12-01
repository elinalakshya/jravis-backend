import logging
from openai import OpenAI
from publishers.affiliate_funnel_publisher import save_funnel_page

logger = logging.getLogger("AffiliateFunnelEngine")
client = OpenAI()


def generate_affiliate_funnel():
    """JRAVIS generates a complete high-income affiliate funnel."""
    prompt = """
    Create a complete affiliate funnel page for a high-ticket digital product.
    Use this structure:
    - Title
    - Emotional hook
    - Problem statement
    - Product introduction (use placeholder AFFILIATE_LINK)
    - 5 key benefits
    - Step-by-step how it works
    - Social proof (imaginary testimonials)
    - Strong call to action with AFFILIATE_LINK
    Format everything in clean HTML.
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return r.choices[0].message["content"]


def parse_title(html_content):
    """Extracts title from AI-generated HTML."""
    try:
        start = html_content.find("<h1>")
        end = html_content.find("</h1>")
        return html_content[start+4:end].strip()
    except:
        return "Affiliate_Funnel_Page"


def run_affiliate_funnel_engine():
    """Main engine that generates and saves funnels."""
    logger.info("📣 Running Affiliate Funnel Engine...")

    try:
        content = generate_affiliate_funnel()
        title = parse_title(content)

        # Replace placeholder with actual affiliate URL later
        final_html = content.replace(
            "AFFILIATE_LINK",
            "https://your-affiliate-link.com"
        )

        save_funnel_page(title, final_html)

        logger.info("✅ Affiliate Funnel Created Successfully")

    except Exception as e:
        logger.error(f"❌ Affiliate Funnel Engine Error: {e}")
