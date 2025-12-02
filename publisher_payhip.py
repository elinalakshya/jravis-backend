import requests
import uuid
from settings import PAYHIP_API_KEY, OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

def publish_payhip_product():
    title = "JRAVIS Auto Product " + str(uuid.uuid4())[:6]

    # 1. Generate description
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Create a product description for a digital asset"}]
    )
    description = response.choices[0].message.content

    print("💰 Payhip Product:", title)

    # 2. Upload a dummy PDF file
    pdf_data = b"%PDF-1.4 TEST"

    files = {
        "file": ("product.pdf", pdf_data, "application/pdf")
    }

    data = {
        "api_key": PAYHIP_API_KEY,
        "title": title,
        "price": "299",
        "description": description
    }

    resp = requests.post(
        "https://payhip.com/api/v1/products",
        data=data,
        files=files
    ).json()

    print("📤 Payhip Published:", resp)
    return resp
