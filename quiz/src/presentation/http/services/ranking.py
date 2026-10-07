from infra.repository.ranking_repository import RankingRepository
from infra.repository.redis_client import RedisClient
import asyncio
import logging
from typing import List

logger = logging.getLogger(__name__)

redis_client = RedisClient("REDIS_URL")
repository = RankingRepository(redis_client)


async def get_ranking(difficulty: str):
    logger.info("Coletando ranking")
    return await repository.get_ranking(difficulty)


async def set_ranking(ranking_front: List, difficulty: str):
    logger.info("setando ranking")

    ranking_databases = get_ranking(difficulty)

    ranking = ranking_front + ranking_databases

    ranking = sorted(ranking, key=lambda x: x['score'], reverse=True)

    return await repository.set_ranking(ranking, difficulty)