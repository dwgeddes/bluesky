import os, logging
from PIL import Image

def convert_to_jpeg(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        jpeg_path = os.path.splitext(image_path)[0] + ".jpeg"
        img.convert("RGB").save(jpeg_path, format="JPEG", quality=85)
        return jpeg_path
    except Exception as e:
        logging.error(f"Error converting image: {e}")
        raise Exception(f"Error converting image: {e}")
