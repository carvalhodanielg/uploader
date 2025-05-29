import pytest
import base64
from io import BytesIO
from PIL import Image
from src import generate_caption
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_image_path():
    return Path(__file__).parent / "test_images" / "flag.png"

@pytest.mark.usefixtures("capsys")
def create_test_image():
    # Cria uma imagem de teste simples
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr)

@pytest.mark.usefixtures("capsys")
def test_generate_caption(test_image_path):
    # Arrange
    # test_image = create_test_image()
    with open(test_image_path, "rb") as image_file:
        image_bytes = image_file.read()
    teste_image = base64.b64encode(image_bytes)


    # test_image = test_image()

    # Act
    caption = generate_caption(teste_image)
    
    logger.info("caption: %s", caption)
    # Assert
    assert isinstance(caption, str)
    assert len(caption) > 0