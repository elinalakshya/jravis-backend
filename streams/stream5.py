import json
import random
import datetime

def run():
    """
    JRAVIS Worker — Stream 5
    Task: Stock Image & Video Concepts (Hybrid Automation)
    Output: JSON
    """

    # High-demand categories
    image_categories = [
        "Business Meeting",
        "Fitness & Health",
        "AI Technology",
        "Work From Home",
        "Travel Landscape",
        "Food Photography",
        "Office Workspace",
        "Luxury Lifestyle",
        "Minimal Aesthetic Scenes",
        "Nature Macro Shot",
    ]

    video_categories = [
        "Cinematic B-Roll",
        "Slow Motion Food Shot",
        "City Timelapse",
        "Nature Footage",
        "Typing on Keyboard",
        "Product Showcase Shot",
        "Fitness Exercise Clip",
        "Aesthetic Home Office Clip",
        "Emotional People Closeup",
        "Car Driving POV",
    ]

    # Styles for images and videos
    styles = [
        "modern aesthetic",
        "clean minimal",
        "cinematic",
        "vibrant color palette",
        "soft neutral tones",
        "bold contrast lighting",
        "retro vintage film look",
        "ultra realistic"
    ]

    # JRAVIS generates both images & videos
    num_images = random.randint(5, 10)
    num_videos = random.randint(3, 6)

    image_list = []
    video_list = []

    # Generate image concepts
    for i in range(num_images):
        category = random.choice(image_categories)
        style = random.choice(styles)
        image_list.append({
            "id": f"stock_image_{i+1}",
            "category": category,
            "style": style,
            "prompt": f"{category} in {style} style, high resolution, sharp focus.",
            "title": f"{category} — {style.title()}",
            "tags": [
                category.replace(" ", "-").lower(),
                "stock-photo",
                style.replace(" ", "-"),
                "ai-photo"
            ],
            "created_at": str(datetime.datetime.utcnow())
        })

    # Generate video concepts
    for i in range(num_videos):
        category = random.choice(video_categories)
        style = random.choice(styles)
        video_list.append({
            "id": f"stock_video_{i+1}",
            "category": category,
            "style": style,
            "instructions": (
                f"Shoot/Generate: {category} in {style} style. "
                "Use stable motion, clean framing, 4K resolution."
            ),
            "title": f"{category} — {style.title()}",  
            "tags": [
                category.replace(" ", "-").lower(),
                "stock-video",
                style.replace(" ", "-"),
                "b-roll"
            ],
            "created_at": str(datetime.datetime.utcnow())
        })

    output = {
        "stream": "stock_images_videos",
        "status": "completed",
        "total_images": num_images,
        "total_videos": num_videos,
        "images": image_list,
        "videos": video_list,
        "mode": "hybrid",
        "note": (
            "JRAVIS generated image & video concepts. "
            "Manual Step: Use AI image/video generator (Midjourney, Runway, Pika) "
            "then upload final media to Wirestock, Pexels, Pixabay or Adobe Stock."
        ),
        "timestamp": str(datetime.datetime.utcnow())
    }

    print(json.dumps(output, indent=4))
