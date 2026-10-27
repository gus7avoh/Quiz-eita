import json


class RankingRepository:
    def __init__(self, redis_client) -> None:
        self.redis = redis_client.client

    async def get_ranking(self, difficulty: str) -> dict:
        result = await self.redis.get(f"ranking-{difficulty}")
        if result is None:
            return {"ranking": []}

        return json.loads(result)

    async def add_ranking(self, entry: dict) -> None:
        difficulty = entry["difficulty"]
        ranking_data = await self.get_ranking(difficulty)
        ranking = ranking_data["ranking"]
        existing_entry = next(
            (item for item in ranking if item["quiz_uuid"] == entry["quiz_uuid"]),
            None,
        )
        if existing_entry is None:
            ranking.append(entry)
        else:
            existing_entry.update(entry)
        ranking.sort(key=lambda item: item["score"], reverse=True)

        await self.redis.set(f"ranking:{difficulty}", json.dumps({"ranking": ranking}))
