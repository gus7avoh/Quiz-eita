import logging

from infra.repository.ranking_repository import RankingRepository
from infra.repository.redis_client import RedisClient

logger = logging.getLogger(__name__)

redis_client = RedisClient("REDIS_URL")
ranking_repository = RankingRepository(redis_client)


async def get_ranking(difficulty: str) -> dict:
    logger.info("Coletando ranking dificuldade=%r", difficulty)
    return await ranking_repository.get_ranking(difficulty)


async def add_ranking_entry(entry: dict) -> None:
    await ranking_repository.add_ranking(entry)
    logger.info(
        "Registro adicionado ao ranking dificuldade=%r nome=%s",
        entry["dificuldade"],
        entry["nome"],
    )


async def delete_ranking(difficulty: str) -> bool:
    logger.info("Excluindo ranking dificuldade=%r", difficulty)
    return await ranking_repository.delete_ranking(difficulty)
