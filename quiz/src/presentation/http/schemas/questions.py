from pydantic import BaseModel, Field


class QuizQuestionResponse(BaseModel):
    enunciado: str = Field(min_length=1)
    alternativas: list[str] = Field(min_length=1)


class QuizQuestionsResponse(BaseModel):
    perguntas: list[QuizQuestionResponse] = Field(min_length=1)


class QuizQuestionsRequest(BaseModel):
    uuid: str
