from pydantic import BaseModel, Field


class AnswerToInterpret(BaseModel):
    """Uma resposta falada e as alternativas contra as quais ela será comparada."""

    user_response: str = Field(min_length=1)
    alternatives: list[str] = Field(min_length=1)


class InterpretedAnswer(BaseModel):
    """Resultado da interpretação de uma resposta."""

    user_response: str = Field(min_length=1)
    alternatives: list[str] = Field(min_length=1)
    referential_alternative: str | None = None


class InterpretAnswer(BaseModel):
    """Resultado em lote, na mesma ordem das entradas recebidas."""

    answers: list[InterpretedAnswer] = Field(min_length=1)
