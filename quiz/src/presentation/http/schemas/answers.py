from pydantic import BaseModel, Field


class QuizAnswerRequest(BaseModel):
    uuid: str
    enunciado: str = Field(min_length=1)
    resposta_usuario: str = Field(min_length=1)


class QuizAnswer(BaseModel):
    resposta: str = Field(min_length=1)
    correta: bool
    explicacao: str = Field(min_length=1)


class QuizAnswerResponse(BaseModel):
    resposta: QuizAnswer
