import requests
from PDFImageClass import PDFImageEmbedder
from util import InputValidator

class BikeDataProcessor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.pdf_embedder = PDFImageEmbedder()

    def fetch_bike_data(self, params):
        page = 1
        all_bikes = []
        while True:
            params['page'] = page
            full_url = InputValidator.create_url(self.base_url, params)
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                if not data.get('bikes'):
                    break
                all_bikes.extend(data.get('bikes', []))
                page += 1
            else:
                print(f"Request failed with status code: {response.status_code}")
                print(f"Response text: {response.text}")
                break
        return all_bikes

    def filter_and_group_bikes(self, bikes, years, months, manufacturer):
        grouped_bikes = {}
        filtered_images = []
        for bike in bikes:
            date_stolen = bike.get('date_stolen')
            if date_stolen and InputValidator.is_within_years_months(date_stolen, years, months):
                manufacturer_name = bike["manufacturer_name"].lower()
                if manufacturer_name not in grouped_bikes:
                    grouped_bikes[manufacturer_name] = []
                grouped_bikes[manufacturer_name].append(bike)
                if manufacturer_name.lower() == manufacturer:
                    bike_image = bike.get('large_img')
                    filtered_images.append(bike_image)
        return grouped_bikes, filtered_images

    def fetch_images(self, image_urls):
        images = []
        for url in image_urls:
            image = self.pdf_embedder.fetch_image(url)
            if image:
                images.append(image)
            else:
                print("Failed to fetch image:", url)
        return images

    def create_pdf_with_images(self, images):
        if images:
            self.pdf_embedder.embed_images_in_pdf(images)
            base64PDF = self.pdf_embedder.encode_pdf_to_base64()
            # Uncomment below for base64PDF
            # print("base64PDF: ", base64PDF)
        else:
            print("No valid images to embed in PDF.")

    def get_manufacturer_details(self, grouped_bikes, manufacturer=None):
        manufacturer_url = "https://bikeindex.org/api/v3/manufacturers/"
        keys_to_process = [manufacturer] if manufacturer else grouped_bikes.keys()
        for key in keys_to_process:
            full_url = f"{manufacturer_url}{key}"
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                print(data)
            else:
                print(f"Request failed for manufacturer {key} with status code: {response.status_code}")
                print(f"Response text: {response.text}")
