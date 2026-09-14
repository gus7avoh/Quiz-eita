from src.domain.entities.quiz import Quiz


class QuizDTO:

    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def sort_questions(self):
        pass
    

    def get_question(self, enunciado: str):
        pass


    def is_correct_answer(self, enunciado: str, resposta_usuario: str):
        pass


    def get_answer(
        self,
        enunciado: str,
        resposta_usuario: str
    ):
        pass