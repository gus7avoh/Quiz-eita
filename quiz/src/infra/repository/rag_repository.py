import json

class RagRepository:
    def __init__(self, redis_client):
        self.redis = redis_client.client

    async def create(
        self,
        id_drive: str,
        chunk: int,
        name: str,
        document_type: str,
        date_modification: str,
        text: str,
        embedding: list[float]
    ):
        await self.redis.set(
            f"id_drive:{id_drive}:chunk:{chunk}",
            json.dumps({
                "name": name,
                "document_type": document_type,
                "date_modification": date_modification,
                "text": text,
                "embedding": embedding
            })
        )

    async def get(self, id_drive: str, chunk: int):
        result = await self.redis.get(f"id_drive:{id_drive}:chunk:{chunk}")

        if result is None:
            return None

        return json.loads(result)
    
    
    async def list_documents(self):
        documents = {}

        async for key in self.redis.scan_iter(match="id_drive:*:chunk:*"):
            data = await self.redis.get(key)

            if data is None:
                continue

            document = json.loads(data)

            id_drive = key.split(":")[1]

            documents[id_drive] = {
                "date_modification": document["date_modification"]
            }

        return documents
    

    async def delete(self, id_drive: str, chunk: int):
        await self.redis.delete(f"id_drive:{id_drive}:chunk:{chunk}")

    async def delete_document(self, id_drive: str):
        keys = [
            key
            async for key in self.redis.scan_iter(
                match=f"id_drive:{id_drive}:chunk:*"
            )
        ]

        if keys:
            await self.redis.delete(*keys)
        
        








