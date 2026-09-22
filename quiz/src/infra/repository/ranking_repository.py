from typing import List
import json


class RankingRepository:
    def __init__(self, redis_client) -> None:
        self.redis = redis_client

    def get_ranking(self, difficulty: str):
        return self.redis.get(f"ranking:{difficulty}")

    async def set_ranking(self, ranking:List, difficulty: str):
        await self.redis.set(
            f"ranking:{difficulty}",
            json.dumps({
                "ranking": ranking
            })
        )