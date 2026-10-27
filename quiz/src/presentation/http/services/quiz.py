import asyncio
import logging

from app.graph.graph import graph
from domain.entities.InterpretAnswer import AnswerToInterpret
from domain.entities.quiz import Quiz
from infra.repository.quiz_repository import QuizRepository
from infra.repository.redis_client import RedisClient
from presentation.http.dto.quiz_dto import QuizDTO
from presentation.http.services.interpret_answer import interpret_answer
from presentation.http.utils.uuid import generate_quiz_uuid

logger = logging.getLogger(__name__)

redis_client = RedisClient("REDIS_URL")
repository = QuizRepository(redis_client)


async def create_quiz(tema: str, quantidade: int, dificuldade: str):
    uuid = generate_quiz_uuid()
    try:
        logger.info(
            "Criando quiz uuid=%s tema=%r quantidade=%s dificuldade=%r",
            uuid,
            tema,
            quantidade,
            dificuldade,
        )
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
        result = await graph.ainvoke(
            {
                "tema": tema,
                "quantidade": quantidade,
                "dificuldade": dificuldade,
                "perguntas": [],
            }
        )

        quiz = Quiz(**result)

        await repository.complete(uuid, quiz.model_dump())
        logger.info("Quiz concluído uuid=%s", uuid)

    except Exception as e:
        logger.exception("Falha ao processar quiz uuid=%s", uuid)
        await repository.fail(uuid, str(e))


async def get_quiz(
    quiz_uuid: str,
):
    try:
        if await status_check(quiz_uuid) != "completed":
            return None

        logger.info("Coletando quiz uuid=%s", quiz_uuid)
        data = await repository.get_quiz(quiz_uuid)

        quiz = Quiz(**data["quiz"])
        quiz_dto = QuizDTO(quiz)

        return quiz_dto.get_question()

    except Exception as e:
        logger.exception("Falha ao processar quiz uuid=%s", quiz_uuid)
        await repository.fail(quiz_uuid, str(e))


async def delete_quiz(list_uuid: list[str]):
    try:
        for item in list_uuid:
            await repository.delete(item.uuid)

        return {"excluded": True}

    except Exception as e:
        logger.exception("Falha ao processar quiz uuid=%s", item.uuid)
        await repository.fail(item.uuid, str(e))


async def answer_quiz(quiz_uuid: str, enunciado: str, resposta: str):
    try:
        if await status_check(quiz_uuid) != "completed":
            return None

        logger.info("Coletando quiz uuid=%s", quiz_uuid)
        data = await repository.get_quiz(quiz_uuid)

        quiz = Quiz(**data["quiz"])
        quiz_dto = QuizDTO(quiz)

        literal_answer = quiz_dto.get_answer(enunciado, resposta)
        if literal_answer is not None:
            return literal_answer

        question = quiz_dto.find_question(enunciado)
        if question is None:
            return None

        interpreted = await interpret_answer(
            [
                AnswerToInterpret(
                    user_response=resposta,
                    alternatives=question.alternativas,
                )
            ]
        )
        resolved_answer = interpreted.answers[0].referential_alternative
        if resolved_answer is None:
            logger.warning(
                "Não foi possível relacionar a resposta à pergunta uuid=%s",
                quiz_uuid,
            )
            return None

        return quiz_dto.get_answer(enunciado, resolved_answer)

    except Exception:
        logger.exception("Falha ao processar quiz uuid=%s", quiz_uuid)
        raise


async def status_check(quiz_uuid: str):
    logger.info("Checando status do quiz uuid=%s", quiz_uuid)

    data = await repository.get_quiz(quiz_uuid)

    status = data["status"]

    if status in ("completed", "failed"):
        return status

    return "processing"
