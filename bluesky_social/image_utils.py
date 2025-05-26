"""
Image utilities for BlueSky posts.

This module provides functions for working with images in BlueSky posts,
including format conversion and optimization.
"""

import logging
import os
from typing import Optional

from PIL import Image, UnidentifiedImageError

from .config import DEFAULT_JPEG_QUALITY


def convert_to_jpeg(image_path: str, quality: Optional[int] = None) -> str:
    """
    Convert an image to JPEG format for upload to BlueSky.

    Args:
        image_path: Path to the source image file
        quality: JPEG quality (1-100), defaults to DEFAULT_JPEG_QUALITY

    Returns:
        Path to the converted JPEG file

    Raises:
        FileNotFoundError: If the source image file does not exist
        UnidentifiedImageError: If the file is not a valid image
        Exception: For other image processing errors
    """
    if quality is None:
        quality = DEFAULT_JPEG_QUALITY
    if not os.path.exists(image_path):
        error_msg = f"Image file not found: {image_path}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        img = Image.open(image_path)
        jpeg_path = os.path.splitext(image_path)[0] + ".jpeg"

        # Convert to RGB (removing alpha channel if present)
        if img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        ):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Save as JPEG with specified quality
        img.save(jpeg_path, format="JPEG", quality=quality, optimize=True)
        logging.debug(f"Successfully converted {image_path} to JPEG")
        return jpeg_path

    except UnidentifiedImageError as e:
        error_msg = f"Not a valid image file: {image_path}"
        logging.error(error_msg)
        raise UnidentifiedImageError(error_msg) from e

    except Exception as e:
        error_msg = f"Error converting image {image_path}: {e}"
        logging.error(error_msg, exc_info=True)
        raise Exception(error_msg) from e
