import logging
from src.engines.openai_helper import ask_openai

logger = logging.getLogger("AutoBloggingEngine")


def run_auto_blogging_engine():
    logger.info("🟦 Running Auto Blogging Engine...")

    try:
        system_prompt = (
            "You are JRAVIS, an SEO blogging expert. "
            "Write articles that are legal, unique, helpful, and high ranking. "
            "Avoid plagiarism, avoid health/medical/dangerous claims."
        )

        user_prompt = """
        Generate a long-form SEO blog article with:
        - Title (H1)
        - Introduction
        - 5 detailed sections
        - Bullet points
        - FAQ section
        - Conclusion
        Produce valid HTML for blog publishing.
        """

        html = ask_openai(system_prompt, user_prompt)

        if "JRAVIS_ERROR" in html:
            logger.error("❌ Auto Blogging generation failed.")
            return

        file_data = {
            "filename": "blog_article.html",
            "content": html,
            "type": "html"
        }

        output = {
            "engine": "auto_blogging",
            "status": "success",
            "title": "Blog Article",
            "description": "SEO optimized auto-generated blog article.",
            "html": html,
            "text": None,
            "keywords": ["blog", "SEO", "content", "jrvis"],
            "files": [file_data],
            "metadata": {
                "category": "blogging",
                "platform": "universal",
                "word_count": "1000+"
            }
        }

        logger.info("✅ Blog Article Generated Successfully")
        return output

    except Exception as e:
        logger.error(f"❌ Auto Blogging Engine Error: {e}")
