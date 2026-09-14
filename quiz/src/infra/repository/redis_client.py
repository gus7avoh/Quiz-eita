import redis.asyncio as redis
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")


class RedisClient:
    def __init__(self) -> None:
        redis_url = getenv("REDIS_URL")
        if not redis_url:
            raise RuntimeError("REDIS_URL não foi configurada")
        self.client = redis.from_url(redis_url, decode_responses=True)

    def get_connection(self):
        return self.client
