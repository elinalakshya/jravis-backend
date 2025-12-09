import os
from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify

def run_publishers(title, description, extracted_dir):
    file_path = f"{extracted_dir}/{title}.zip"
    results = []

    if os.getenv("GUMROAD_API_KEY"):
        results.append(publish_to_gumroad(title, description, file_path))

    if os.getenv("PAYHIP_API_KEY"):
        results.append(publish_to_payhip(title, description, file_path))

    if os.getenv("PRINTIFY_API_KEY"):
        results.append(publish_to_printify(title, description, file_path))

    return results
