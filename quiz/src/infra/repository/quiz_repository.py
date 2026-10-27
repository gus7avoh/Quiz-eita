import json


class QuizRepository:
    def __init__(self, redis_client):
        self.redis = redis_client.client

    async def create(
        self, quiz_id: str, player_name: str, difficulty: str
    ) -> None:
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps(
                {
                    "status": "processing",
                    "player_name": player_name,
                    "score": 0,
                    "difficulty": difficulty,
                    "scored_questions": [],
                },
                ensure_ascii=False,
            ),
        )

    async def complete(self, quiz_id: str, quiz: dict):
        stored_quiz = await self.get_quiz(quiz_id) or {}
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps(
                {
                    **stored_quiz,
                    "status": "completed",
                    "quiz": quiz,
                },
                ensure_ascii=False,
            ),
        )

    async def get_quiz(self, quiz_id: str):
        result = await self.redis.get(f"quiz:{quiz_id}")

        if result is None:
            return None

        return json.loads(result)

    async def save_ranking_data(
        self,
        quiz_id: str,
        player_name: str,
        score: int,
        difficulty: str,
    ) -> None:
        quiz_data = await self.get_quiz(quiz_id)
        if quiz_data is None:
            raise LookupError(f"Quiz {quiz_id} não encontrado")

        quiz_data.update(
            {
                "player_name": player_name,
                "score": score,
                "difficulty": difficulty,
            }
        )
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps(quiz_data, ensure_ascii=False),
        )

    async def record_correct_answer(self, quiz_id: str, question: str) -> int:
        quiz_data = await self.get_quiz(quiz_id)
        if quiz_data is None:
            raise LookupError(f"Quiz {quiz_id} não encontrado")

        scored_questions = quiz_data.setdefault("scored_questions", [])
        if question in scored_questions:
            return quiz_data["score"]

        scored_questions.append(question)
        quiz_data["score"] += 1
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps(quiz_data, ensure_ascii=False),
        )
        return quiz_data["score"]

    async def fail(self, quiz_id: str, error: str):
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps(
                {"status": "failed", "error": error},
                ensure_ascii=False,
            ),
        )

    async def delete(self, quiz_id: str):
        await self.redis.delete(f"quiz:{quiz_id}")
