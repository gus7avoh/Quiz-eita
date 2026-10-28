from pydantic import BaseModel, Field


class RankingEntryRequest(BaseModel):
    player_name: str = Field(min_length=1)
    quiz_uuid: str = Field(min_length=1)
    score: int = Field(ge=0)
    difficulty: str = Field(min_length=1)


class RankingEntry(BaseModel):
    player_name: str
    quiz_uuid: str
    score: int
    difficulty: str


class RankingResponse(BaseModel):
    ranking: list[RankingEntry]


class RankingCreatedResponse(BaseModel):
    created: bool


class RankingDeleteResponse(BaseModel):
    deleted: bool
