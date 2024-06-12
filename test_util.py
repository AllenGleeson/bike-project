import pytest
from datetime import datetime, timedelta
from util import InputValidator

@pytest.fixture
def mock_input(monkeypatch):
    inputs = iter(["banff", "1", "6", "10", "ktm"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

def test_get_user_input(mock_input):
    location, years, months, distance, manufacturer = InputValidator.get_user_input()
    assert location == "banff"
    assert years == 1
    assert months == 6
    assert distance == 10
    assert manufacturer == "ktm"

def test_is_within_years_months_true():
    current_time = datetime.now()
    target_date = current_time - timedelta(days=(1 * 365 + 6 * 30))  # 1 year and 6 months ago
    target_timestamp = int(target_date.timestamp())

    timestamp_within_range = target_timestamp + 1  # Within the range
    assert InputValidator.is_within_years_months(timestamp_within_range, 1, 6) is True

def test_is_within_years_months_false():
    current_time = datetime.now()
    target_date = current_time - timedelta(days=(1 * 365 + 6 * 30 + 1))  # 1 year, 6 months, and 1 day ago
    target_timestamp = int(target_date.timestamp())

    timestamp_outside_range = target_timestamp - 1  # Outside the range
    assert InputValidator.is_within_years_months(timestamp_outside_range, 1, 6) is False

def test_create_url():
    base_url = "https://bikeindex.org/api/v3/search?per_page=100&stolenness=proximity"
    params = {'location': 'banff', 'distance': 10}
    expected_url = "https://bikeindex.org/api/v3/search?per_page=100&stolenness=proximity&location=banff&distance=10"
    assert InputValidator.create_url(base_url, params) == expected_url

if __name__ == "__main__":
    pytest.main()