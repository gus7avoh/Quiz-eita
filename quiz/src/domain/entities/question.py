from pydantic import BaseModel, Field


class Question(BaseModel):
    id: int | None = Field(
        default=None,
        description="Identificador da pergunta dentro do quiz"
    )

    enunciado: str = Field(
        description="Texto da pergunta do quiz"
    )


class QuestionSet(BaseModel):
    perguntas: list[Question] = Field(
        description="Perguntas geradas para o quiz"
    )

