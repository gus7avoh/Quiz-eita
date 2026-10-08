# from app.graph.graph import graph
# import asyncio

# import json
# import os

# from infra.repository.redis_client import RedisClient

# def main():
#     # result = graph.invoke({
#     #     "tema": "Paraiso perdido",
#     #     "quantidade": 4,
#     #     "dificuldade": "mista",
#     #     "perguntas": [],
#     # })

#     # dados = {
#     #     **result,
#     #     "perguntas": [
#     #         pergunta.model_dump()
#     #         for pergunta in result["perguntas"]
#     #     ]
#     # }

#     # arquivo = os.path.join(
#     #     # "C:\\cod\\Quiz-eita\\quiz\\src\\presentation\\response.json"
#     #     "D:\\cod\\eita\\quiz\\src\\presentation\\response.json"
#     # )

#     # with open(arquivo, "w", encoding="utf-8") as f:
#     #     json.dump(
#     #         dados,
#     #         f,
#     #         ensure_ascii=False,
#     #         indent=4
#     #     )


        
#     redis_client = RedisClient()
#     conn = redis_client.get_connection()

#     async def test_redis():
#         print(await conn.ping())


#     asyncio.run(test_redis())


# if __name__ == "__main__":
#     main()




import asyncio

from infra.repository.redis_client import RedisClient
from infra.repository.quiz_repository import QuizRepository
from app.graph.node.retrive_context import retrieve_context

async def main():
    
    await retrieve_context({"context": []})

asyncio.run(main())



