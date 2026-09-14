from presentation.http.utils.uuid import generate_quiz_uuid
from presentation.http.dto.quizDTO import QuizDTO
from infra.repository.quiz_repository import QuizRepository
from infra.repository.redis_client import RedisClient
from app.graph.graph import graph
from domain.entities.quiz import Quiz
import asyncio
import logging


logger = logging.getLogger(__name__)


async def create_quiz(tema: str, quantidade: int, dificuldade: str):
    uuid = generate_quiz_uuid()
    try:
        logger.info("Criando quiz uuid=%s tema=%r quantidade=%s dificuldade=%r", uuid, tema, quantidade, dificuldade)
        redis_client = RedisClient()
        repository = QuizRepository(redis_client)
        await repository.create(uuid)
        
        asyncio.create_task(
            process_quiz(
                uuid,
                repository,
                tema,
                quantidade,
                dificuldade,
            )
        )
    
        logger.info("Quiz aceito para processamento uuid=%s", uuid)
        return uuid
    except Exception:
        logger.exception("Falha ao criar quiz uuid=%s", uuid)
        raise
    
    
async def process_quiz(
    uuid: str,
    repository: QuizRepository,
    tema: str,
    quantidade: int,
    dificuldade: str,
):
    try:
        logger.info("Processando quiz uuid=%s", uuid)
        result = await asyncio.to_thread(
            graph.invoke,
            {
                "tema": tema,
                "quantidade": quantidade,
                "dificuldade": dificuldade,
                "perguntas": [],
            }
        )

        quiz = Quiz(**result)

        await repository.complete(
            uuid,
            quiz.model_dump()
        )
        logger.info("Quiz concluído uuid=%s", uuid)

    except Exception as e:
        logger.exception("Falha ao processar quiz uuid=%s", uuid)
        await repository.fail(uuid, str(e))
    

async def get_quiz():
    pass


async def delete_quiz():
    pass


async def answer_quiz():
    pass
