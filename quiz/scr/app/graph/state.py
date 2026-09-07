from typing import TypedDict

from domain.entities.quiz import Pergunta


class QuizState(TypedDict):
    tema: str
    quantidade: int
    dificuldade: str
    perguntas: list[Pergunta]