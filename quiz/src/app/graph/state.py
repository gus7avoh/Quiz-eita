from typing import Any, TypedDict

from domain.entities.quiz import Pergunta


class QuizState(TypedDict):
    tema: str
    quantidade: int
    dificuldade: str
    perguntas: list[Pergunta]
    context: list[str, Any]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self[key] = value