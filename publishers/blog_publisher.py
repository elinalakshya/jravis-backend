import os
import logging

logger = logging.getLogger("BlogPublisher")

BASE_OUTPUT = "output/blog"

CATEGORIES = ["AI", "Income", "Health", "Mixed"]

# Ensure folders exist
for c in CATEGORIES:
    os.makedirs(os.path.join(BASE_OUTPUT, c), exist_ok=True)


def save_blog_post(category, title, html_content, md_content):
    """Save blog posts as HTML and Markdown in the correct category folder."""

    safe_title = title.replace(" ", "_").replace("/", "_")

    html_path = os.path.join(BASE_OUTPUT, category, safe_title + ".html")
    md_path = os.path.join(BASE_OUTPUT, category, safe_title + ".md")

    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"📄 Saved blog: {html_path} and {md_path}")
        return html_path, md_path

    except Exception as e:
        logger.error(f"❌ Error saving blog files: {e}")
        return None, None
