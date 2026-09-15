from domain.entities.quiz import Quiz
import random


class QuizDTO:

    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def sort_alternatives(self, alternatives: list):
        random.shuffle(alternatives)
        return alternatives

    def get_question(self):
        return {
            "perguntas": [
                {
                    "enunciado": question.enunciado,
                    "alternativas": self.sort_alternatives(
                        question.alternativas.copy()
                    )
                }
                for question in self.quiz.perguntas
            ]
        }

    def is_correct_answer(
        self,
        question,
        resposta_usuario: str
    ):
        return question.resposta == resposta_usuario

    def get_answer(
        self,
        enunciado: str,
        resposta_usuario: str
    ):
        for question in self.quiz.perguntas:
            if question.enunciado == enunciado:
                return {
                    "resposta": {
                        "resposta": question.resposta,
                        "correta": self.is_correct_answer(
                            question,
                            resposta_usuario
                        ),
                        "explicacao": question.explicacao
                    }
                }
            
        return None
