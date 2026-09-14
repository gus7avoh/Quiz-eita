from presentation.http.utils.uuid import generate_quiz_uuid
from presentation.http.dto.quizDTO import QuizDTO
from infra.repository.quiz_repository import QuizRepository
from infra.repository.redis_client import RedisClient
from app.graph.graph import graph
from domain.entities.quiz import Quiz
import asyncio
import logging


logger = logging.getLogger(__name__)

redis_client = RedisClient()
repository = QuizRepository(redis_client)


async def create_quiz(tema: str, quantidade: int, dificuldade: str):
    uuid = generate_quiz_uuid()
    try:
        logger.info("Criando quiz uuid=%s tema=%r quantidade=%s dificuldade=%r", uuid, tema, quantidade, dificuldade)
        await repository.create(uuid)
        
        asyncio.create_task(
            process_quiz(
                uuid,
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
    

async def get_quiz(
        quiz_uuid: str,
    ):
    try:
        if (await status_check(quiz_uuid) != "completed"):
            return None
        
        logger.info("Coletando quiz uuid=%s", quiz_uuid)
        data = await repository.get_quiz(quiz_uuid)

        quiz = Quiz(**data["quiz"])
        quiz_dto = QuizDTO(quiz)

        return quiz_dto.get_question()

    except Exception as e:
        logger.exception("Falha ao processar quiz uuid=%s", quiz_uuid)
        await repository.fail(quiz_uuid, str(e))


async def delete_quiz():
    pass


async def answer_quiz():
    pass


async def status_check(quiz_uuid: str): 
    logger.info("Checando status do quiz uuid=%s", quiz_uuid)

    data = await repository.get_quiz(quiz_uuid)

    status = data["status"]

    if status in ("completed", "failed"):
        return status

    return "processing"