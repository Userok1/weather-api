import pytest
from redis import Redis
from redis.exceptions import ConnectionError

import app.src.redis_cache as rc_module
from app.src.dependencies import send_request
from app.src.redis_cache import RedisManager


def test_send_request_bad_redis_host(monkeypatch):
    mock_redis_client = Redis("badid:badport")
    
    redis_manager = RedisManager(mock_redis_client) 
    
    def mock_get_redis_manager(*args, **kwargs):
        return redis_manager
    
    monkeypatch.setattr(rc_module, "client", mock_get_redis_manager)
    
    with pytest.raises(ConnectionError):
        send_request("Moscow")