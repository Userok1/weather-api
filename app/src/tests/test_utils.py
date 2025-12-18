import pytest
from typing import Any
import requests

from app.src.utils import request_weather
from app.config import get_config
from app.src.exceptions import NoMatchingLocationError

config = get_config()


@pytest.fixture
def data_to_return():
    return {
        "location": {
            "name": "Moscow"
        },
        "current": {
            "temp_c": "-5.7",
            "feelslike_c": "-12.7", 
            "temp_f": "21.7",
            "feelslike_f": "9,2"
        }
    }
    

@pytest.fixture
def params_from_request() -> tuple[str, dict[str, str]]:
    return config.URL, {"key": config.API_KEY, "q": "Moscow"}


def test_request_weather_with_proper_data_format(monkeypatch, data_to_return, params_from_request):
    class MockResponse:
        def __init__(self, *args, **kwargs):
            self.status_code = 200

        def json(self):
            return data_to_return
        

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    url, params = params_from_request
    response = request_weather(url=url, params=params)

    assert response['name'] == "Moscow"
    assert response['temp_c'] == "-5.7"
    assert response['feelslike_c'] == "-12.7"
    assert response['temp_f'] == "21.7"
    assert response['feelslike_f'] == "9,2"
    

def test_request_weather_raises_error(monkeypatch, params_from_request):
    def mock_raise_error(*args, **kwargs):
        raise NoMatchingLocationError    
    
    monkeypatch.setattr(requests, "get", mock_raise_error)
    url, params = params_from_request

    with pytest.raises(NoMatchingLocationError):
        request_weather(url=url, params=params)