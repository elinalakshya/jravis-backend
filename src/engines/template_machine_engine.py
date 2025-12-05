import logging
from src.engines.openai_helper import ask_openai
from publishers.template_machine_publisher import save_template_machine_file

logger = logging.getLogger("TemplateMachineEngine")

def run_template_machine_engine():
    logger.info("🟦 Running Template Machine Engine...")

    system_prompt = """
    Generate a ready-to-use editable template for any business task.
    Output:
    - Title
    - Use Case
    - Step-by-step instructions
    - Editable text blocks
    """

    user_prompt = "Create a universal editable template for entrepreneurs."

    try:
        content = ask_openai(system_prompt, user_prompt)

        save_template_machine_file(content)

        logger.info("✅ Template Machine blueprints generated.")
    except Exception as e:
        logger.error(f"❌ Template Machine Engine Error: {e}")
