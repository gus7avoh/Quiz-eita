from fastapi import APIRouter, HTTPException
from presentation.http.schemas import (
    RankingCreatedResponse,
    RankingDeleteResponse,
    RankingEntryRequest,
    RankingResponse,
)
from presentation.http.services.ranking import (
    add_ranking_entry as add_ranking_entry_service,
)
from presentation.http.services.ranking import (
    delete_ranking as delete_ranking_service,
)
from presentation.http.services.ranking import get_ranking as get_ranking_service

router = APIRouter(
    prefix="/ranking",
    tags=["ranking"],
)


@router.get("/{difficulty}", response_model=RankingResponse)
async def get_ranking(difficulty: str) -> RankingResponse:
    ranking_data = await get_ranking_service(difficulty)
    return RankingResponse(**ranking_data)


@router.post("", response_model=RankingCreatedResponse)
async def add_ranking_entry(
    data: RankingEntryRequest,
) -> RankingCreatedResponse:
    try:
        await add_ranking_entry_service(data.model_dump())
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    return RankingCreatedResponse(added=True)


@router.delete("/{difficulty}", response_model=RankingDeleteResponse)
async def delete_ranking(difficulty: str) -> RankingDeleteResponse:
    deleted = await delete_ranking_service(difficulty)
    return RankingDeleteResponse(deleted=deleted)
