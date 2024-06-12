# Stolen Bike API Search

## Tools needed to run the code
![Python Version](https://img.shields.io/badge/python%20version-python%203.8%2B-brightgreen)

Python 3.8.10

## To run code:
- Create Virtual Environment: Run command: python -m venv myenv
- Activate Virtual Environment: Run command: myenv\Scripts\activate
- Run command: pip install requirements.txt. Use python 3.8 to create the virtual environment
- Run command: python main.py
- Enter the location, duration(in years and months), distance from the location and the manufacturer.
- Enter 0 for years or months if years but no months or months but no years.
- If you want all manufacturers then leave manufacturer blank and press enter.

To see base64 pdf images uncomment line 59 of BikeDataProcessor.py inside create_pdf_with_images.

## To run tests:
- Run command: pytest

##### Author: Allen Gleeson
##### Email: allen_gleeson@hotmail.com