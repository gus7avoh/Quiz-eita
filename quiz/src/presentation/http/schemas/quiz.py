from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    tema: str = Field(min_length=1)
    quantidade: int = Field(gt=0)
    dificuldade: str = Field(min_length=1)


class QuizCreatedResponse(BaseModel):
    uuid: str


class QuizQuestionResponse(BaseModel):
    enunciado: str = Field(min_length=1)
    alternativas: list[str] = Field(min_length=1)


class QuizQuestionsResponse(BaseModel):
    perguntas: list[QuizQuestionResponse] = Field(min_length=1)

    
class QuizQuestionsRequest(BaseModel):
    uuid: str


class QuizAnswerRequest(BaseModel):
    enunciado: str = Field(min_length=1)
    resposta_usuario: str = Field(min_length=1)
