from typing import Any

from domain.entities.question import QuestionSet


def build_contextual_quiz_prompt(
    state: dict,
    question_set: QuestionSet,
    relevant_context: list[dict[str, Any]],
) -> str:
    questions = "\n".join(
        f"Pergunta {question.id}: {question.enunciado}"
        for question in question_set.perguntas
    )
    context_by_question = []
    for question_context in relevant_context:
        question_id = question_context.get("question_id")
        contexts = question_context.get("contexts", [])
        context_text = "\n".join(
            f"- {chunk.get('text', '')}"
            for chunk in contexts
            if chunk.get("text")
        ) or "Nenhum contexto relevante foi encontrado."
        context_by_question.append(
            f"CONTEXTO DA PERGUNTA {question_id}:\n{context_text}"
        )

    context = "\n\n".join(context_by_question)
    if not context:
        context = "Nenhum contexto relevante foi encontrado."

    return f"""
    Gere um quiz completo para as perguntas abaixo priorizando o contexto
    fornecido.

    Tema: {state["tema"]}
    Dificuldade: {state["dificuldade"]}

    PERGUNTAS:
    {questions}

    CONTEXTO:
    {context}

    REGRAS:
    - Retorne exatamente uma pergunta para cada enunciado recebido.
    - Preserve os enunciados recebidos sem alterar seu significado.
    - Gere exatamente quatro alternativas para cada pergunta.
    - Gere exatamente uma resposta correta para cada pergunta.
    - A resposta correta deve ser uma das quatro alternativas.
    - Gere uma explicação objetiva para cada resposta correta.
    - Use o contexto como fonte principal para criar as alternativas, respostas
      e explicações.
    - Quando o contexto não trouxer informação suficiente para responder uma
      pergunta, use o conhecimento geral e o treinamento-base do modelo como
      complemento.
    - Mesmo usando conhecimento-base, mantenha a resposta relacionada ao tema,
      à pergunta e ao nível de dificuldade solicitados.
    - Não apresente como informação do contexto algo que não esteja nele.
    - Nunca deixe uma pergunta sem alternativas, resposta ou explicação.
    """
