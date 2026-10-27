import logging

from infra.repository.quiz_repository import QuizRepository
from infra.repository.ranking_repository import RankingRepository
from infra.repository.redis_client import RedisClient

logger = logging.getLogger(__name__)

redis_client = RedisClient("REDIS_URL")
quiz_repository = QuizRepository(redis_client)
ranking_repository = RankingRepository(redis_client)


async def get_ranking(difficulty: str) -> dict:
    logger.info("Coletando ranking dificuldade=%r", difficulty)
    return await ranking_repository.get_ranking(difficulty)


async def add_ranking_entry(entry: dict) -> None:
    await quiz_repository.save_ranking_data(
        quiz_id=entry["quiz_uuid"],
        player_name=entry["player_name"],
        score=entry["score"],
        difficulty=entry["difficulty"],
    )
    await ranking_repository.add_ranking(entry)
    logger.info(
        "Registro adicionado ao ranking dificuldade=%r quiz_uuid=%s",
        entry["difficulty"],
        entry["quiz_uuid"],
    )


async def delete_ranking(difficulty: str) -> bool:
    logger.info("Excluindo ranking dificuldade=%r", difficulty)
    return await ranking_repository.delete_ranking(difficulty)