from pydantic import BaseModel, Field


class RankingEntryRequest(BaseModel):
    """Payload enviado pelo frontend quando a partida termina."""

    nome: str = Field(min_length=1)
    pontos: int = Field(ge=0)
    dificuldade: str = Field(min_length=1)


class RankingEntry(BaseModel):
    nome: str
    pontos: int
    dificuldade: str


class RankingResponse(BaseModel):
    ranking: list[RankingEntry]


class RankingCreatedResponse(BaseModel):
    added: bool


class RankingDeleteResponse(BaseModel):
    deleted: bool
