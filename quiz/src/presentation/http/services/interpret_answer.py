import logging
import time
from collections.abc import Sequence

from app.prompts import interpret_answer_prompt
from domain.entities.InterpretAnswer import (
    AnswerToInterpret,
    InterpretedAnswer,
    InterpretAnswer,
)
from infra.llm.gemini_client import GeminiClient
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)


async def interpret_answer(
    answers: Sequence[AnswerToInterpret | dict],
) -> InterpretAnswer:
    """Interpreta várias respostas em uma única chamada ao modelo.

    A ordem dos itens retornados corresponde à ordem dos itens recebidos.
    Alternativas que não forem reconhecidas retornam None.
    """
    inputs = [
        answer
        if isinstance(answer, AnswerToInterpret)
        else AnswerToInterpret.model_validate(answer)
        for answer in answers
    ]
    if not inputs:
        raise ValueError("É necessário informar ao menos uma resposta")

    started_at = time.perf_counter()
    try:
        prompt = interpret_answer_prompt(inputs)
        response = await GeminiClient().invoke(
            [HumanMessage(content=prompt)],
            structured_output=InterpretAnswer,
        )

        parsed = (
            response
            if isinstance(response, InterpretAnswer)
            else InterpretAnswer.model_validate(response)
        )

        if len(parsed.answers) != len(inputs):
            raise ValueError(
                "A IA retornou uma quantidade de respostas diferente da entrada"
            )

        normalized_answers = []
        for answer_input, answer_output in zip(inputs, parsed.answers):
            selected = answer_output.referential_alternative
            if selected is not None and selected not in answer_input.alternatives:
                logger.warning(
                    "A IA retornou uma alternativa inexistente; resposta ignorada"
                )
                selected = None

            normalized_answers.append(
                InterpretedAnswer(
                    user_response=answer_input.user_response,
                    alternatives=answer_input.alternatives,
                    referential_alternative=selected,
                )
            )

        return InterpretAnswer(answers=normalized_answers)

    except Exception:
        logger.exception("Falha ao interpretar respostas do usuário")
        raise
    finally:
        logger.info(
            "Interpretação de respostas finalizada em %.3f segundos",
            time.perf_counter() - started_at,
        )
