import random

from domain.entities.quiz import Pergunta, Quiz


class QuizDTO:

    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def sort_alternatives(self, alternatives: list[str]) -> list[str]:
        random.shuffle(alternatives)
        return alternatives

    def get_question(self) -> dict:
        return {
            "perguntas": [
                {
                    "enunciado": question.enunciado,
                    "alternativas": self.sort_alternatives(
                        question.alternativas.copy()
                    ),
                }
                for question in self.quiz.perguntas
            ]
        }

    def find_question(self, enunciado: str) -> Pergunta | None:
        return next(
            (
                question
                for question in self.quiz.perguntas
                if question.enunciado == enunciado
            ),
            None,
        )

    def is_literal_answer(
        self,
        question: Pergunta,
        resposta_usuario: str,
    ) -> bool:
        return resposta_usuario in question.alternativas

    def is_correct_answer(
        self,
        question: Pergunta,
        resposta_usuario: str,
    ) -> bool:
        return question.resposta == resposta_usuario

    def get_answer(
        self,
        enunciado: str,
        resposta_usuario: str,
    ) -> dict | None:
        """Monta a resposta somente quando a alternativa já foi resolvida.

        A interpretação por IA é assíncrona e fica no serviço de aplicação.
        Este DTO permanece síncrono e determinístico.
        """
        question = self.find_question(enunciado)
        if question is None or not self.is_literal_answer(
            question,
            resposta_usuario,
        ):
            return None

        return {
            "resposta": {
                "resposta": question.resposta,
                "correta": self.is_correct_answer(
                    question,
                    resposta_usuario,
                ),
                "explicacao": question.explicacao,
            }
        }
