import os
import json
import logging
from PIL import Image, ImageDraw, ImageFont

from db import get_db

logging.basicConfig(level=logging.INFO)

IMAGE_DIR = "/opt/render/project/src/data/images"
os.makedirs(IMAGE_DIR, exist_ok=True)


# ---------------------------------------------------
# Generate image for a single product
# ---------------------------------------------------

def generate_image_for_product(product_id: str) -> str:
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT payload FROM products WHERE id=?", (product_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        raise Exception(f"❌ Product not found: {product_id}")

    product = json.loads(row[0])
    title = product.get("title", "JRAVIS PRODUCT")

    # Create simple image
    img = Image.new("RGB", (800, 800), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()

    draw.multiline_text(
        (40, 300),
        title,
        fill=(20, 20, 20),
        font=font,
        spacing=8
    )

    image_path = os.path.join(IMAGE_DIR, f"{product_id}.png")
    img.save(image_path)

    conn.close()

    logging.info(f"🖼️ Image generated: {image_path}")

    return image_path


# ---------------------------------------------------
# Generate images for all products
# ---------------------------------------------------

def generate_images_for_all_products():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM products")
    rows = cur.fetchall()

    generated = []
    skipped = 0

    for (product_id,) in rows:
        image_path = os.path.join(IMAGE_DIR, f"{product_id}.png")

        if os.path.exists(image_path):
            skipped += 1
            continue

        try:
            path = generate_image_for_product(product_id)
            generated.append({
                "product_id": product_id,
                "image_path": path
            })
        except Exception as e:
            logging.error(f"❌ Failed generating image for {product_id}: {e}")

    conn.close()

    return {
        "generated": len(generated),
        "skipped": skipped,
        "images": generated
}

