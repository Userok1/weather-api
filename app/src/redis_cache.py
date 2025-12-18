import redis
from typing import Any
import json

from app.config import get_config

config = get_config()
client = redis.from_url(config.REDIS_URL)


class RedisManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, redis_client: redis.Redis) -> None:
        self.client = redis_client        
    

    def save_data(self, city: str, weather_data: dict[str, Any]) -> dict[str, Any]:
        serialized_data = json.dumps(weather_data)
        
        result = self.client.hset("weather", city, serialized_data)
        
        return {
            "success": True,
            "name": city,
            "is_new": result == 1
        }
        

    def read_data(self, city: str) -> dict[str, Any]:
        cache_data = self.client.hget("weather", city)
        try:
            deserialized_cache_data = json.loads(cache_data)
            return deserialized_cache_data
        except TypeError as e:
            print(e)
            return None
    

    def set_expire(self, expire: int) -> bool:
        r = self.client.expire("weather", time=expire)
        return r
    
    
def get_redis_manager():
    redis_client = redis.from_url(config.REDIS_URL)
    return RedisManager(redis_client)


if __name__ == "__main__":
    res = client.ping()
    print(res)