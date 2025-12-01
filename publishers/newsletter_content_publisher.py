import os
import logging

logger = logging.getLogger("NewsletterContentPublisher")

OUTPUT = "output/newsletter_issues"
os.makedirs(OUTPUT, exist_ok=True)


def save_newsletter_issue(title, html, md):
    """Saves newsletter issue in both HTML + Markdown formats."""
    safe_title = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe_title)
    os.makedirs(folder, exist_ok=True)

    try:
        # Save HTML
        html_path = os.path.join(folder, "newsletter.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Save Markdown
        md_path = os.path.join(folder, "newsletter.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)

        logger.info(f"📧 Newsletter Issue Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving newsletter content: {e}")
        return None
