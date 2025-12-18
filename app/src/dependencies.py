import json
from redis.exceptions import ConnectionError
from typing import Any
from redis import Redis

from app.src.utils import request_weather
from app.config import get_config
from app.src.exceptions import NoMatchingLocationError
from app.src.redis_cache import get_redis_manager

config = get_config()
client = get_redis_manager()


def send_request(city: str, exp: int = 300) -> dict[str, Any]:
    try:
        params = {"key": config.API_KEY, "q": city}
        cache_data = client.read_data(city)
        if cache_data:
            return cache_data

        try:
            data = request_weather(config.URL, params)  
        except NoMatchingLocationError as e:
            print(e)
            return

        client.save_data(city, data)
        client.set_expire(expire=exp)
        return data
    except ConnectionError as e:
        raise ConnectionError("Bad host or server is not running")


if __name__ == "__main__":
    city = "Moscow"
    rc = Redis("lskdjflskajfslkfj:87129837129873")
    rc.get("key")