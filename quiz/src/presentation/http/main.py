from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Quiz Eita"}

"""
PLANO DA API — QUIZ-EITA

Objetivo:
    Criar uma API assíncrona para geração de quizzes utilizando o LangGraph.
    O frontend não ficará esperando a IA terminar a geração. Ele iniciará
    o processamento através de um POST e consultará o resultado através
    de um GET.

FLUXO PRINCIPAL:

1. POST /quiz
    - Receber o estado necessário para gerar o quiz.
    - Validar os dados recebidos.
    - Gerar um identificador único (UUID) para essa execução.
    - Criar um registro no Redis com status "processing".
    - Iniciar o processamento do LangGraph em segundo plano.
    - Retornar imediatamente o UUID para o frontend.
    - HTTP Status: 202 Accepted.

    Exemplo de resposta:
    {
        "id": "8f7a9c..."
    }


2. PROCESSAMENTO DO QUIZ
    - Utilizar o UUID para identificar a execução.
    - Executar o LangGraph.
    - O LangGraph será responsável pela geração do quiz através do Gemini.
    - Caso a geração seja concluída:
        - Salvar o resultado no Redis.
        - Alterar o status para "completed".
    - Caso ocorra um erro:
        - Salvar a informação do erro.
        - Alterar o status para "failed".


3. GET /quiz/{id}
    - Receber o UUID da execução.
    - Buscar o registro correspondente no Redis.
    - Se ainda estiver processando:
        {
            "id": "8f7a9c...",
            "status": "processing"
        }

    - Se tiver terminado:
        {
            "id": "8f7a9c...",
            "status": "completed",
            "quiz": {
                "perguntas": [...]
            }
        }

    - Se tiver ocorrido um erro:
        {
            "id": "8f7a9c...",
            "status": "failed",
            "error": "..."
        }

    - Se o UUID não existir:
        - Retornar HTTP 404.


REDIS:

    Cada execução terá uma chave própria:

        quiz:{uuid}

    Exemplo:

        quiz:8f7a9c...

    O Redis será utilizado como armazenamento temporário do estado
    e resultado das execuções.

    Os registros deverão possuir TTL para evitar que quizzes antigos
    permaneçam armazenados indefinidamente.


ARQUITETURA:

    presentation/
        http/
            routes/
            schemas/

                ↓

    application/
        services/
        use_cases/

                ↓

    app/
        graph/

                ↓

    infra/
        llm/
        repositories/

    O acesso ao Redis deverá ser abstraído através de um repositório,
    evitando que as regras da aplicação dependam diretamente do Redis.

    Exemplo conceitual:

        QuizRepository
             ↑
             |
        RedisQuizRepository


FLUXO COMPLETO:

    FRONTEND
       |
       | POST /quiz
       | State
       ↓
    API
       |
       | gera UUID
       ↓
    REDIS
       |
       | status = processing
       ↓
    API retorna 202 + UUID
       |
       ↓
    PROCESSAMENTO EM BACKGROUND
       |
       ↓
    LANGGRAPH
       |
       ↓
    GEMINI
       |
       ↓
    QUIZ GERADO
       |
       ↓
    REDIS
       |
       | status = completed
       | quiz = resultado
       ↓
    FRONTEND
       |
       | GET /quiz/{uuid}
       ↓
    API
       |
       ↓
    RESULTADO


IMPORTANTE:

    O POST NÃO deve executar o LangGraph de forma síncrona aguardando
    a resposta da IA.

    O objetivo é separar:

        "iniciar a geração"
            de
        "consultar o resultado da geração"

    Dessa forma, o frontend pode fazer polling no GET até que o status
    seja "completed" ou "failed".

    Futuramente, o polling poderá ser substituído por WebSocket,
    Server-Sent Events ou outro mecanismo de comunicação em tempo real,
    caso seja necessário.
"""