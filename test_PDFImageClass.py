import pytest
from unittest.mock import MagicMock, patch
from PDFImageClass import PDFImageEmbedder
from PIL import Image
import io

@pytest.fixture
def embedder():
    return PDFImageEmbedder()

def test_fetch_image(embedder, monkeypatch):
    # Create a mock image content
    image_content = Image.new('RGB', (60, 30), color='red')
    byte_arr = io.BytesIO()
    image_content.save(byte_arr, format='JPEG')
    image_bytes = byte_arr.getvalue()

    # Mock the requests.get function
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.content = image_bytes

    def mock_requests_get(url):
        if url == "https://example.com/image.jpg":
            return mock_response
        raise Exception("Invalid URL")

    monkeypatch.setattr('requests.get', mock_requests_get)

    # Test with a valid URL
    image = embedder.fetch_image("https://example.com/image.jpg")
    assert image is not None
    assert image.mode == "RGB"

    # Test with an invalid URL
    try:
        invalid_image = embedder.fetch_image("invalid_url")
    except Exception:
        invalid_image = None
    assert invalid_image is None

def test_embed_images_in_pdf(embedder, monkeypatch):
    # Mock the Image.open, FPDF, and os.remove methods
    with patch('PDFImageClass.Image.open') as mock_open, \
         patch('PDFImageClass.FPDF.add_page') as mock_add_page, \
         patch('PDFImageClass.FPDF.image') as mock_image, \
         patch('PDFImageClass.os.remove') as mock_remove:
        # Mock the return value of Image.open
        mock_open.side_effect = [MagicMock(mode="RGB") for _ in range(3)]

        # Test with a list of mock images
        images = [MagicMock() for _ in range(3)]
        embedder.embed_images_in_pdf(images)

        # Assert that FPDF methods are called the correct number of times
        assert mock_add_page.call_count == len(images) + 1  # including initial page
        assert mock_image.call_count == len(images)

        # Assert that os.remove is called for each image
        assert mock_remove.call_count == len(images)

def test_encode_pdf_to_base64(embedder, monkeypatch):
    # Mock the open function to return bytes
    mock_open = MagicMock()
    mock_open.return_value.__enter__.return_value.read.return_value = b"mocked_pdf_content"
    monkeypatch.setattr('builtins.open', mock_open)

    # Test the base64 encoding
    encoded_pdf = embedder.encode_pdf_to_base64()
    assert encoded_pdf is not None
    assert isinstance(encoded_pdf, str)

if __name__ == "__main__":
    pytest.main()