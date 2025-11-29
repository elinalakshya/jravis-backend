import requests
import uuid
from settings import GUMROAD_TOKEN, OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

def publish_gumroad_product():
    # 1. Generate title + description
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": "Generate a digital product idea, title and 2-paragraph description"}
        ]
    )

    text = response.choices[0].message.content
    title = "JRAVIS Product " + str(uuid.uuid4())[:6]

    print("📦 Gumroad product:", title)

    # 2. Create product
    create_url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": GUMROAD_TOKEN,
        "name": title,
        "description": text,
        "price": 299
    }
    product = requests.post(create_url, data=data).json()
    print("🛒 Gumroad Create:", product)

    product_id = product["product"]["id"]

    # 3. Upload a simple file
    pdf_content = b"%PDF-1.4 test content"
    upload = requests.post(
        f"https://api.gumroad.com/v2/products/{product_id}/files",
        data={"access_token": GUMROAD_TOKEN},
        files={"file": ("jr_test.pdf", pdf_content, "application/pdf")}
    ).json()

    print("📤 File Uploaded:", upload)

    return product
