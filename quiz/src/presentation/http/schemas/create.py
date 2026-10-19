from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    tema: str = Field(min_length=1)
    quantidade: int = Field(gt=0)
    dificuldade: str = Field(min_length=1)


class QuizCreatedResponse(BaseModel):
    uuid: str
