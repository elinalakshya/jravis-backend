from product_factory import generate_product


def run_all_streams_micro_engine():
    """
    Draft-only engine.
    Generates product pack and returns metadata.
    """
    product = generate_product()
    return product
