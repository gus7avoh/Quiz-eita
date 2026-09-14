import json

class QuizRepository:
    def __init__(self, redis_client):
        self.redis = redis_client.client

    async def create(self, quiz_id: str):
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps({
                "status": "processing"
            })
        )


    async def complete(self, quiz_id: str, quiz: dict):
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps({
                "status": "completed",
                "quiz": quiz
            })
        )


    async def get_quiz(self, quiz_id: str):
        result = await self.redis.get(f"quiz:{quiz_id}")


        print("DATA repo:", result)
        print("TYPE repo:", type(result))

        if result is None:
            return None

        return json.loads(result)
    

    async def fail(self, quiz_id: str, error: str):
        await self.redis.set(
            f"quiz:{quiz_id}",
            json.dumps({
                "status": "failed",
                "error": error
            })
        )


    async def delete(self, quiz_id: str):
        await self.redis.delete(f"quiz:{quiz_id}")