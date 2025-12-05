import logging
from src.engines.openai_helper import ask_openai
from publishers.blog_publisher import save_blog_article

logger = logging.getLogger("AutoBlogEngine")

def run_auto_blogging_engine():
    logger.info("🟦 Running Auto Blogging Engine...")

    system_prompt = """
    You are JRAVIS — expert SEO article generator.
    Create:
    - Blog title
    - SEO meta description
    - 800–1200 word long article
    - Headings and subheadings
    - Keywords section
    """

    user_prompt = "Write an SEO blog post on a trending topic."

    try:
        content = ask_openai(system_prompt, user_prompt)

        save_blog_article(content)

        logger.info("✅ Auto-blog article generated.")
    except Exception as e:
        logger.error(f"❌ Auto Blogging Error: {e}")
