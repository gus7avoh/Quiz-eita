import logging
from typing import Any

from langchain_core.messages import HumanMessage
from sklearn.metrics.pairwise import cosine_similarity

from app.graph.state import QuizState
from app.prompts import (
    c_sharp_prompt,
    build_contextual_quiz_prompt,
    famosos_prompt,
    filmes_prompt,
    java_prompt,
    java_script_prompt,
    jogos_prompt,
    musicas_prompt,
    python_prompt,
    quiz_prompt_generic,
    quiz_question_only,
)
from domain.entities.question import QuestionSet
from domain.entities.quiz import Quiz
from infra.llm.gemini_client import GeminiClient
from infra.llm.gemini_embedding_client import GeminiEmbeddingClient


PROMPTS_TEMAS = {
    "python": python_prompt,
    "java": java_prompt,
    "javascript": java_script_prompt,
    "c#": c_sharp_prompt,
    "filmes": filmes_prompt,
    "jogos": jogos_prompt,
    "músicas": musicas_prompt,
    "famosos": famosos_prompt,
}

gemini_client = GeminiClient()
embedding_client = GeminiEmbeddingClient()

logger = logging.getLogger(__name__)


def is_contextual_flow(state: QuizState) -> bool:
    return bool(state.get("context"))


def build_question_prompt(state: QuizState) -> str:
    tema = state.get("tema", "").strip().lower()
    prompt = quiz_question_only(state)
    prompt_theme = PROMPTS_TEMAS.get(tema)

    if prompt_theme:
        prompt += prompt_theme()

    return prompt


def approximate_question_embeddings(
    question_embeddings: list[list[float]],
    document_context: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Relaciona cada pergunta aos chunks mais similares do documento."""
    if not question_embeddings or not document_context or top_k <= 0:
        return []

    context_embeddings = [
        chunk["embedding"]
        for chunk in document_context
    ]
    similarities = cosine_similarity(
        question_embeddings,
        context_embeddings,
    )

    relevant_context = []
    for question_id, scores in enumerate(similarities):
        ranked_indices = scores.argsort()[::-1][:top_k]
        relevant_context.append({
            "question_id": question_id,
            "contexts": [
                {
                    **{
                        key: value
                        for key, value in document_context[index].items()
                        if key != "embedding"
                    },
                    "similarity": float(scores[index]),
                }
                for index in ranked_indices
            ],
        })

    return relevant_context


def assign_question_ids(question_set: QuestionSet) -> QuestionSet:
    for question_id, question in enumerate(question_set.perguntas):
        question.id = question_id

    return question_set


def generate_generic_quiz(state: QuizState) -> dict[str, Any]:
    prompt = quiz_prompt_generic(state)
    response = gemini_client.invoke(
        [HumanMessage(content=prompt)],
        structured_output=Quiz,
    )

    return {"perguntas": response.perguntas}


async def generate_contextual_quiz(state: QuizState) -> dict[str, Any]:
    question_prompt = build_question_prompt(state)
    question_response = gemini_client.invoke(
        [HumanMessage(content=question_prompt)],
        structured_output=QuestionSet,
    )

    question_response = assign_question_ids(question_response)
    questions = question_response.perguntas
    question_texts = [question.enunciado for question in questions]
    question_embeddings = await embedding_client.create_embedding(question_texts)

    relevant_context = approximate_question_embeddings(
        question_embeddings,
        state.get("context", []),
    )

    contextual_quiz_prompt = build_contextual_quiz_prompt(
        state,
        question_response,
        relevant_context,
    )
    quiz_response = gemini_client.invoke(
        [HumanMessage(content=contextual_quiz_prompt)],
        structured_output=Quiz,
    )

    return {"perguntas": quiz_response.perguntas}


async def generate_quiz(state: QuizState) -> dict[str, Any]:
    try:
        if is_contextual_flow(state):
            logger.info("Iniciando geração de quiz contextual")
            return await generate_contextual_quiz(state)

        logger.info("Iniciando geração de quiz genérico")
        return generate_generic_quiz(state)
    except Exception:
        logger.exception("Falha no node generate_quiz")
        raise
