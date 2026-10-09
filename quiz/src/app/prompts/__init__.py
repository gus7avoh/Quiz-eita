from .comum import quiz_prompt_generic
from .rag import build_contextual_quiz_prompt, quiz_question_only
from .rag.especificos import (
    c_sharp_prompt,
    famosos_prompt,
    filmes_prompt,
    java_prompt,
    java_script_prompt,
    jogos_prompt,
    musicas_prompt,
    python_prompt,
)

quiz_prompt = quiz_prompt_generic
