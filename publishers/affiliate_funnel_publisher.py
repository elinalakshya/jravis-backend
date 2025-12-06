import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AFFILIATE_BASE_URL = "https://your-affiliate-domain.com/?ref="  # optional

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_funnel_content(product_title, product_url, affiliate_code=None):
    """
    Generates a complete affiliate funnel / blog article promoting a product.
    """

    # Build affiliate link if provided
    final_url = product_url
    if affiliate_code:
        final_url = f"{product_url}?aff={affiliate_code}"

    prompt = f"""
    Write a highly persuasive affiliate marketing funnel article promoting:
    Product: {product_title}
    Link: {final_url}

    Requirements:
    - Conversational, human, friendly tone
    - NOT detectable as AI generated
    - Include benefits, emotional triggers, clear call-to-action
    - 300–500 words
    - Add “Get Started” CTA with link
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write premium human-like marketing funnels."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )

        article = completion.choices[0].message.content
        return {
            "status": "success",
            "content": article,
            "url": final_url
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def save_funnel_html(title, content, out_dir="funnels"):
    """
    Saves the article as an HTML landing page.
    """

    os.makedirs(out_dir, exist_ok=True)

    filename = title.lower().replace(" ", "-") + ".html"
    filepath = os.path.join(out_dir, filename)

    html = f"""
    <html>
    <head>
        <title>{title} - Funnel</title>
    </head>
    <body>
    <h1>{title}</h1>
    <div>{content}</div>
    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return {"status": "success", "file": filepath}
