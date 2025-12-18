import pytest
from redis import Redis
import json

from app.src.redis_cache import RedisManager


@pytest.fixture
def data_to_return():
    return {
        "name": "Moscow",
        "temp_c": "-5.7",
        "feelslike_c": "-12.7", 
        "temp_f": "21.7",
        "feelslike_f": "9,2"
    }
    

def test_save_data(monkeypatch, data_to_return):

    def mock_hset(*args, **kwargs):
        return 1
    
    redis_client_mock = Redis()
    
    monkeypatch.setattr(redis_client_mock, "hset", mock_hset) 

    client = RedisManager(redis_client_mock)
    city, weather_data = data_to_return['name'], data_to_return
    result = client.save_data(city=city, weather_data=weather_data)

    assert result["success"] is True
    assert result["name"] == data_to_return["name"]
    assert result["is_new"] is True
    

def test_read_data(monkeypatch, data_to_return):

    def mock_hget(*args, **kwargs):
        return json.dumps(data_to_return)
    
    redis_client = Redis()

    monkeypatch.setattr(Redis, "hget", mock_hget)
    
    rm = RedisManager(redis_client=redis_client)
    result = rm.read_data("Moscow") 

    assert result['name'] == 'Moscow' 
    assert result['temp_c'] == '-5.7' 
    assert result['feelslike_c'] == '-12.7' 
    assert result['temp_f'] == '21.7' 
    assert result['feelslike_f'] == '9,2' 