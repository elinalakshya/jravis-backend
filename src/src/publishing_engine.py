from publisher_payhip import publish_to_payhip


def run_publishers(title, description, zip_path):
    print("💼 RUNNING PUBLISHERS (PAYHIP DEBUG MODE)")

    result = {}

    try:
        debug = publish_to_payhip(
            title=title,
            description=description,
            file_path=zip_path,
            price=199,
        )
        result["payhip"] = debug
    except Exception as e:
        result["payhip"] = {"exception": str(e)}

    return result

