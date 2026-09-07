from pydantic import BaseModel, Field


class Pergunta(BaseModel):
    enunciado: str = Field(
        description="Texto da pergunta do quiz"
    )

    alternativas: list[str] = Field(
        description="Quatro alternativas possíveis"
    )

    resposta: str = Field(
        description="Alternativa correta"
    )

    explicacao: str = Field(
        description="Explicação da resposta correta"
    )


class Quiz(BaseModel):
    perguntas: list[Pergunta] = Field(
        description="Lista de perguntas do quiz"
    )