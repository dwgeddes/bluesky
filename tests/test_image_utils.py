import os
from PIL import Image
import tempfile
import pytest
from image_utils import convert_to_jpeg

def test_convert_to_jpeg(tmp_path):
    # Create a temporary image file
    file_path = tmp_path / "test.png"
    image = Image.new("RGB", (100, 100), color="red")
    image.save(file_path)
    jpeg_path = convert_to_jpeg(str(file_path))
    assert os.path.exists(jpeg_path)
    # Clean up created jpeg file
    os.remove(jpeg_path)
