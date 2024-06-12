from InputValidator import InputValidator
from BikeDataProcessor import BikeDataProcessor

def main():
    base_url = "https://bikeindex.org/api/v3/search?per_page=100&stolenness=proximity"
    location, years, months, distance, manufacturer = InputValidator.get_user_input()
    params = {
        'location': location,
        'distance': distance,
    }
    processor = BikeDataProcessor(base_url)
    bikes = processor.fetch_bike_data(params)
    grouped_bikes, filtered_images = processor.filter_and_group_bikes(bikes, years, months, manufacturer)
    images = processor.fetch_images(filtered_images)
    processor.create_pdf_with_images(images)

    if manufacturer:
        print("grouped_bikes:", grouped_bikes.get(manufacturer, []))
    else:
        print("grouped_bikes:", grouped_bikes)

    processor.get_manufacturer_details(grouped_bikes, manufacturer)

if __name__ == "__main__":
    main()