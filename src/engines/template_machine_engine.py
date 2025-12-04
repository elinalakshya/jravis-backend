import logging
from src.engines.openai_helper import ask_openai

logger = logging.getLogger("TemplateMachineEngine")


def run_template_machine_engine():
    logger.info("🟦 Running Template Machine Engine...")

    try:
        # Prompts
        system_prompt = (
            "You are JRAVIS, a template machine generator. "
            "Output must include editable blocks and clear structure."
        )

        user_prompt = """
        Generate a multi-section template package:
        - Title
        - Editable blocks (in HTML)
        - Notes for customization
        - Instructions
        Produce a clean HTML file suitable for digital marketplaces.
        """

        html = ask_openai(system_prompt, user_prompt)

        if "JRAVIS_ERROR" in html:
            logger.error("❌ Template Machine generation failed.")
            return

        # File storage
        file_data = {
            "filename": "template_machine.html",
            "content": html,
            "type": "html"
        }

        output = {
            "engine": "template_machines",
            "status": "success",
            "title": "Template Machine Output",
            "description": "JRAVIS-generated editable digital template.",
            "html": html,
            "text": None,
            "keywords": ["template", "digital", "machine"],
            "files": [file_data],
            "metadata": {
                "category": "templates",
                "platform": "universal",
                "price": "5 - 20 USD"
            }
        }

        logger.info("✅ Template Machine Template Created Successfully")
        return output

    except Exception as e:
        logger.error(f"❌ Template Machine Engine Error: {e}")
