def quiz_prompt(state: dict):
    return f"""
    Crie {state["quantidade"]} perguntas de quiz.

    Tema: {state["tema"]}
    Dificuldade: {state["dificuldade"]}

    REGRAS GERAIS:

    Cada pergunta deve possuir:
    - um enunciado claro e objetivo
    - exatamente 4 alternativas
    - exatamente 1 alternativa correta
    - uma explicação da resposta correta

    ALTERNATIVAS:

    - As 4 alternativas devem possuir tamanhos semelhantes.
    - Evite que a alternativa correta seja significativamente maior ou
    mais detalhada que as demais.
    - Não adicione informações desnecessárias às alternativas apenas para
    aumentar ou diminuir seu tamanho.
    - As alternativas devem possuir estrutura e nível de detalhamento
    semelhantes.
    - Todas as alternativas devem pertencer à mesma categoria.
    - Todas devem ser plausíveis dentro do contexto da pergunta.
    - Não utilize alternativas obviamente absurdas ou facilmente descartáveis.
    - Não repita alternativas.
    - Nunca crie duas alternativas que possam ser consideradas corretas.
    - A resposta correta deve estar entre as 4 alternativas.

    DIFICULDADE:

    A dificuldade deve considerar o conhecimento necessário para responder
    à pergunta e não apenas a complexidade da escrita.

    FÁCIL:
    - Deve ser respondível por uma pessoa comum com conhecimento geral
    sobre o tema.
    - Priorize informações populares, conhecidas e frequentemente
    associadas ao tema.
    - Evite detalhes específicos, técnicos ou pouco conhecidos.
    - A resposta deve exigir principalmente reconhecimento ou lembrança
    de uma informação conhecida.
    - Evite exigir múltiplas etapas de raciocínio.

    MÉDIO:
    - Deve exigir algum conhecimento ou familiaridade com o tema.
    - Pode utilizar informações menos óbvias, mas ainda acessíveis para
    alguém que conhece razoavelmente o assunto.
    - Pode exigir comparação, associação ou uma pequena sequência de
    raciocínio.
    - Evite conhecimentos excessivamente específicos ou especializados.

    DIFÍCIL:
    - Deve exigir conhecimento mais aprofundado ou capacidade de
    relacionar diferentes informações do tema.
    - Pode utilizar informações menos conhecidas, detalhes relevantes ou
    exigir raciocínio em múltiplas etapas.
    - Ainda deve ser uma pergunta justa e respondível com base no
    conhecimento relacionado ao tema.
    - Não transforme a dificuldade em uma pergunta obscura, extremamente
    específica ou baseada em uma informação que poucas pessoas
    poderiam conhecer.
    - Evite perguntas que dependam de conhecimento profissional altamente
    especializado, a menos que isso seja explicitamente solicitado.

    MISTA:
    - Deve combinar perguntas fáceis, médias e difíceis.
    - A distribuição das perguntas deve seguir aproximadamente:
    - 20% fáceis
    - 50% médias
    - 30% difíceis
    - As perguntas devem ser distribuídas ao longo do quiz, evitando
    concentrar todas as perguntas de uma mesma dificuldade.
    - A dificuldade deve ser determinada individualmente para cada pergunta.
    - A quantidade de perguntas de cada nível deve ser a mais próxima
    possível dos percentuais definidos, considerando a quantidade total
    solicitada.

    IMPORTANTE:

    - A dificuldade deve ser consistente entre todas as perguntas.
    - Não torne uma pergunta difícil apenas utilizando uma informação
    extremamente obscura.
    - Não torne uma pergunta fácil apenas porque o enunciado é curto.
    - Priorize perguntas interessantes e relevantes para o tema.
    - Não invente fatos.
    - Não utilize informações que estejam fora do tema solicitado.
    - Cada pergunta deve poder ser compreendida isoladamente.
    - Evite ambiguidades e perguntas que possuam mais de uma resposta
    razoavelmente correta.
    - Não revele a resposta correta através da forma como as alternativas
    são escritas.
    """