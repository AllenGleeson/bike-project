from datetime import datetime, timedelta
import urllib.parse

class InputValidator:
    @staticmethod
    def is_within_years_months(timestamp, years, months):
        current_time = datetime.now()
        # Calculate the date 'years' and 'months' ago from today
        target_date = current_time - timedelta(days=(years * 365 + months * 30))
        target_timestamp = int(target_date.timestamp())
        return timestamp >= target_timestamp

    @staticmethod
    def get_user_input():
        location = input("Enter the location: ")
        # Get duration input: years and months separately
        while True:
            try:
                years = int(input("Enter the duration in years: "))
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for years.")
        while True:
            try:
                months = int(input("Enter the duration in months: "))
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for months.")
        while True:
            try:
                distance = int(input("Enter the distance (as a number, e.g., 5, 10, 15): "))
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for distance.")
        manufacturer = input("Enter the manufacturer: ")
        return location, years, months, distance, manufacturer.lower()

    @staticmethod
    def create_url(base_url, params):
        url_parts = list(urllib.parse.urlparse(base_url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib.parse.urlencode(query)
        return urllib.parse.urlunparse(url_parts)