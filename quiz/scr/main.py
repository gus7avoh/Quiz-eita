from app.graph.graph import graph

import json
import os

def main():
    result = graph.invoke({
        "tema": "Python",
        "quantidade": 2,
        "dificuldade": "difícil",
        "perguntas": [],
    })

    dados = {
        **result,
        "perguntas": [
            pergunta.model_dump()
            for pergunta in result["perguntas"]
        ]
    }

    arquivo = os.path.join(
        "D:\\cod\\eita\\quiz\\scr\\presentation\\response.json"
    )

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            ensure_ascii=False,
            indent=4
        )


if __name__ == "__main__":
    main()