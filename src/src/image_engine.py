import os
from PIL import Image, ImageDraw, ImageFont
from typing import Dict

# Base image directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)


def generate_product_image(product: Dict) -> str:
    """
    Generates a simple branded product image and returns image path.
    """

    width, height = 1024, 1024
    bg_color = (245, 247, 250)   # light gray
    text_color = (20, 20, 20)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Try default font
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        font_title = ImageFont.load_default()
        font_small = ImageFont.load_default()

    title = product.get("title", "Digital Product")
    price = f"₹{product.get('price', '')}"

    # Draw title (wrapped manually)
    y = 200
    max_width = 900
    words = title.split(" ")
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] > max_width:
            draw.text((60, y), line, fill=text_color, font=font_title)
            y += 80
            line = word
        else:
            line = test_line

    if line:
        draw.text((60, y), line, fill=text_color, font=font_title)

    # Footer
    draw.text((60, 850), "JRAVIS DIGITAL", fill=(80, 80, 80), font=font_small)
    draw.text((60, 900), price, fill=(40, 40, 40), font=font_small)

    # Save image
    filename = f"{product['product_id']}.png"
    path = os.path.join(IMAGE_DIR, filename)
    img.save(path, "PNG")

    print("🖼️ Image generated:", path)
    return path
