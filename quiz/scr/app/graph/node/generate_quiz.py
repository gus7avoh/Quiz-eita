from langchain_core.messages import HumanMessage

from app.graph.state import QuizState
from app.prompts import *
from domain.entities.quiz import Quiz
from infra.llm.geminiClient import GeminiClient


PROMPTS_TEMAS = {
    "python": python_prompt,
    "java": java_prompt,
    "javascript": java_script_prompt,
    "c#": c_sharp_prompt,
    "filmes": filmes_prompt,
    "jogos": jogos_prompt,
    "músicas": musicas_prompt,
    "musicas": musicas_prompt,
    "famosos": famosos_prompt,
}


gemini_client = GeminiClient(
    structured_output=Quiz
)


def build_prompt(state: QuizState):
    tema = state.get("tema", "").strip().lower()
    prompt_base = quiz_prompt(state)
    prompt_tema = PROMPTS_TEMAS.get(tema)

    if prompt_tema:
        return prompt_base + prompt_tema()

    return prompt_base


def generate_quiz(state: QuizState):

    print("Iniciando geração de perguntas...")

    prompt = build_prompt(state)

    print("Enviando para o Gemini...")

    response = gemini_client.invoke([
        HumanMessage(content=prompt)
    ])

    print("Resposta gerada...")

    return {
        "perguntas": response.perguntas,
    }