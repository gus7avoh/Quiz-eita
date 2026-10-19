import json
from collections.abc import Sequence

from domain.entities.InterpretAnswer import AnswerToInterpret


def interpret_answer_prompt(
    answers: Sequence[AnswerToInterpret],
) -> str:
    payload = [answer.model_dump() for answer in answers]

    return f"""
Interprete as respostas do usuário em relação às alternativas possíveis.

Para cada item recebido:
- preserve a ordem dos itens;
- escolha exatamente uma alternativa da lista `alternatives`;
- retorne a alternativa completa, exatamente como ela aparece na lista;
- se a fala não corresponder com segurança a uma alternativa, use null em
  `referential_alternative`;
- não crie, corrija ou reformule alternativas.

Responda usando o schema estruturado informado, com um item em `answers` para
cada item de entrada.

Itens:
{json.dumps(payload, ensure_ascii=False)}
"""
