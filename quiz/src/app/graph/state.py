from typing import Any, TypedDict

from domain.entities.quiz import Pergunta


class QuizState(TypedDict, total=False):
    tema: str
    quantidade: int
    dificuldade: str
    perguntas: list[Pergunta]
    context: list[dict[str, Any]]
