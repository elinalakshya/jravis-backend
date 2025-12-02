# publishers/affiliate_blog_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def publish_affiliate_blog(task):
    """
    Generates an SEO affiliate article using OpenAI.
    Upload step is manual because blogs have no universal API.
    """
    print("📝 Creating SEO affiliate article…")

    try:
        prompt = """
        Write a 700-word SEO article reviewing 3 affiliate products.
        Make it fully unique, human-like, and non-AI detectable.
        Do not mention AI anywhere.
        Include headings, subheadings, bullets, and pros/cons.
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        article_text = response.output_text

        # Save to output folder
        output_path = "/opt/render/project/src/generated/affiliate_article.txt"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(article_text)

        print("📄 Affiliate article generated and saved.")
        print("⚠ Manual upload required to WordPress/Webflow.")
        return "Affiliate blog ready"

    except Exception as e:
        print("❌ Affiliate Blog Error:", str(e))
        return "Failed but safe output generated"
