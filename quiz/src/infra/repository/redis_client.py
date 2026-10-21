import redis.asyncio as redis
from os import getenv
from redis.asyncio.retry import Retry
from redis.backoff import NoBackoff

from infra.environment import load_project_environment


load_project_environment()


class RedisClient:
    def __init__(self, env_connection: str) -> None:
        redis_url = getenv(env_connection)
        if not redis_url:
            raise RuntimeError(f"{env_connection} não foi configurada")
        self.client = redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=30,
            retry=Retry(NoBackoff(), retries=1),
        )

    def get_connection(self):
        return self.client
