from product_factory import generate_product


def run_all_streams_micro_engine():
    product = generate_product()
    return {
        "product": product["title"],
        "download_zip": product["zip_path"],
    }
