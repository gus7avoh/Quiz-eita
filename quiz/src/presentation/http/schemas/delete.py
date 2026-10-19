from pydantic import BaseModel, Field


class QuizDeleteRequest(BaseModel):
    uuid: str


class QuizDeleteListRequest(BaseModel):
    list_uuid: list[QuizDeleteRequest] = Field(min_length=1)


class QuizDeleteResponse(BaseModel):
    excluded: bool
