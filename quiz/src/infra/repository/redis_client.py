import redis.asyncio as redis
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")


class RedisClient:
    def __init__(self, env_connection: str) -> None:
        redis_url = getenv(env_connection)
        if not redis_url:
            raise RuntimeError(f"{env_connection} não foi configurada")
        self.client = redis.from_url(redis_url, decode_responses=True)

    def get_connection(self):
        return self.client
