import json
from uuid import uuid4


class RankingRepository:
    """Persists final scores grouped by the selected difficulty."""

    def __init__(self, redis_client) -> None:
        self.redis = redis_client.client

    @staticmethod
    def _key(difficulty: str) -> str:
        return f"ranking:{difficulty}"

    @staticmethod
    def _normalize_entry(entry: dict, difficulty: str) -> dict | None:
        nome = entry.get("nome")
        if not nome:
            return None
        return {
            "id": entry.get("id", str(uuid4())),
            "nome": nome.strip(),
            "pontos": entry["pontos"],
            "dificuldade": entry.get("dificuldade", difficulty),
        }

    async def get_ranking(self, difficulty: str) -> dict:
        result = await self.redis.get(self._key(difficulty))
        if result is None:
            return {"ranking": []}
        data = json.loads(result)
        ranking = [
            normalized
            for item in data.get("ranking", [])
            if (normalized := self._normalize_entry(item, difficulty)) is not None
        ]
        ranking.sort(key=lambda item: item["pontos"], reverse=True)
        return {"ranking": ranking}

    async def add_ranking(self, entry: dict) -> None:
        difficulty = entry["dificuldade"]
        ranking_data = await self.get_ranking(difficulty)
        ranking = ranking_data.setdefault("ranking", [])
        ranking.append(self._normalize_entry(entry, difficulty))
        ranking.sort(key=lambda item: item["pontos"], reverse=True)
        await self.redis.set(
            self._key(difficulty),
            json.dumps({"ranking": ranking}, ensure_ascii=False),
        )

    async def delete_ranking(self, difficulty: str) -> bool:
        deleted_count = await self.redis.delete(self._key(difficulty))
        return deleted_count > 0
