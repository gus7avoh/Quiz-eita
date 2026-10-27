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
            (
                item
                for item in ranking
                if item["quiz_uuid"] == entry["quiz_uuid"]
            ),
            None,
        )
        if existing_entry is None:
            ranking.append(entry)
        else:
            existing_entry.update(entry)
        ranking.sort(key=lambda item: item["score"], reverse=True)

        await self.redis.set(
            f"ranking-{difficulty}",
            json.dumps({"ranking": ranking}, ensure_ascii=False),
        )

    async def update_score(
        self, quiz_uuid: str, difficulty: str, score: int
    ) -> None:
        ranking_data = await self.get_ranking(difficulty)
        entry = next(
            (
                item
                for item in ranking_data["ranking"]
                if item["quiz_uuid"] == quiz_uuid
            ),
            None,
        )
        if entry is None:
            raise LookupError(f"Quiz {quiz_uuid} não está no ranking")

        entry["score"] = score
        ranking_data["ranking"].sort(
            key=lambda item: item["score"],
            reverse=True,
        )
        await self.redis.set(
            f"ranking-{difficulty}",
            json.dumps(ranking_data, ensure_ascii=False),
        )

    async def delete_ranking(self, difficulty: str) -> bool:
        deleted_count = await self.redis.delete(f"ranking-{difficulty}")
        return deleted_count > 0