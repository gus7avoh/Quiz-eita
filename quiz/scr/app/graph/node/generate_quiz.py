from langchain_core.messages import HumanMessage

from app.graph.state import QuizState
from domain.entities.quiz import Quiz
from infra.llm.gemini import create_llm


llm = create_llm()
structured_llm = llm.with_structured_output(Quiz)


def generate_quiz(state: QuizState):

    print("Iniciando geração de perguntas...")

    prompt = f"""
    Crie {state["quantidade"]} perguntas de quiz.

    Tema: {state["tema"]}
    Dificuldade: {state["dificuldade"]}

    Cada pergunta deve possuir:
    - enunciado
    - exatamente 4 alternativas
    - resposta correta
    - explicação da resposta
    """

    print("Enviando para o Gemini...")

    response = structured_llm.invoke([
        HumanMessage(content=prompt)
    ])

    print("Resposta gerada...")

    return {
        "perguntas": response.perguntas,
    }