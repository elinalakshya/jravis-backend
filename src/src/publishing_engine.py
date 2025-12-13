import os
from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify


def run_publishers(title: str, description: str, zip_path: str):
    """
    zip_path MUST be the full path to the zip file.
    Example: factory_output/template-1234.zip
    """

    # 🔒 Normalize path (absolute safety)
    zip_path = os.path.normpath(zip_path)

    # 🛡️ If someone passes a directory, construct zip path safely
    if os.path.isdir(zip_path):
        zip_path = os.path.join(zip_path, f"{title}.zip")

    # 🛡️ Prevent double-zip paths
    if zip_path.endswith(".zip" + os.sep + f"{title}.zip"):
        zip_path = os.path.join(os.path.dirname(zip_path), f"{title}.zip")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    results = []

    if os.getenv("GUMROAD_API_KEY"):
        results.append(
            publish_to_gumroad(title, description, zip_path)
        )

    if os.getenv("PAYHIP_API_KEY"):
        results.append(
            publish_to_payhip(title, description, zip_path)
        )

    if os.getenv("PRINTIFY_API_KEY"):
        results.append(
            publish_to_printify(title, description, zip_path)
        )

    return results
