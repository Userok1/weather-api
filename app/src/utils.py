from typing import Optional
import requests

from app.src.exceptions import NoMatchingLocationError
from app.src.redis_cache import get_redis_manager

client = get_redis_manager()


def request_weather(url: str, params: dict[str, str]) -> Optional[dict[str, str]]:
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        data: dict[str, str] = response.json()
        city: str = data['location']['name']
        temp_c: str = data['current']['temp_c']
        feelslike_c: str = data['current']['feelslike_c']
        temp_f: str = data['current']['temp_f']
        feelslike_f: str = data['current']['feelslike_f']
        return {'name': city, 'temp_c': temp_c, 'feelslike_c': feelslike_c, 
                'temp_f': temp_f, 'feelslike_f': feelslike_f}
    else:
        raise NoMatchingLocationError("No matching location found")


if __name__ == "__main__":
    # print(r)
    res = client.read_data("Kizilurt")
    # cache_data = get_cache_data("Moscow")
    print(res)