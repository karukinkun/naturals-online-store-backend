import os

CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")


def build_image_url(path: str):
    if not path:
        return None
    return f"{CLOUDFRONT_URL}/{path}"
