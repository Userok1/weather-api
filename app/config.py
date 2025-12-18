from dotenv import load_dotenv
import os


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_env()
        return cls._instance

    
    def _load_env(self) -> None:
        load_dotenv()
        self._redis_url = os.getenv('REDIS_URL')
        self._api_key = os.getenv('API_KEY')
        self._weather_url = os.getenv('URL')
        

    @property
    def REDIS_URL(self):
        return self._redis_url
    

    @property
    def API_KEY(self):
        return self._api_key


    @property
    def URL(self):
        return self._weather_url
    

def get_config():
    return Config()