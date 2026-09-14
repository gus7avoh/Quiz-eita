import redis.asyncio as redis
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class RedisClient:
    def __init__(self) -> None:
        self.client = redis.from_url(
            getenv("REDIS_URL"),
            decode_responses=True
        )

    def get_connection(self):
        return self.client