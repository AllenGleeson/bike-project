import os
import base64
import requests
from PIL import Image
from fpdf import FPDF
from io import BytesIO

class PDFImageEmbedder:
    def __init__(self):
        self.output_pdf_path = "output.pdf"

    def fetch_image(self, url):
        """Fetch the image from the URL."""
        if not url or url.lower() == "none":
            print(f"Invalid URL: {url}")
            return None
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return Image.open(BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image from {url}: {e}")
            return None

    def embed_images_in_pdf(self, images):
        """Embed multiple images in a PDF and save it."""
        pdf = FPDF()
        # Counter for generating unique filenames
        img_counter = 0
        for image in images:
            # Convert image to RGB mode if it's in RGBA mode
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            # Add a new page for each image
            pdf.add_page()
            # Save the image temporarily with a unique filename
            img_temp_path = f"temp_image_{img_counter}.jpg"
            image.save(img_temp_path)
            # Add the image to the PDF
            pdf.image(img_temp_path, x=10, y=10, w=100)
            # Increment the counter
            img_counter += 1
            # Remove the temporary image file
            os.remove(img_temp_path)
        # Save the final PDF
        pdf.output(self.output_pdf_path)

    def encode_pdf_to_base64(self):
        """Encode the PDF file to a base64 string."""
        with open(self.output_pdf_path, "rb") as pdf_file:
            pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
        return pdf_base64
