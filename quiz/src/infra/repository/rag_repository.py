import json
from domain.entities.document_chunk import DocumentChunk

class RagRepository:
    def __init__(self, redis_client):
        self.redis = redis_client.client

    async def create(
        self,
        document_chunk: DocumentChunk
    ):
        await self.redis.set(
            f"id_drive:{document_chunk.id_drive}:chunk:{document_chunk.chunk}",
            json.dumps({
                "name": document_chunk.name,
                "document_type": document_chunk.document_type,
                "date_modification": document_chunk.date_modification,
                "text": document_chunk.text,
                "embedding": document_chunk.embedding
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
        
        








