def quiz_question_only(state: dict):
    return f"""
    Crie {state["quantidade"]} perguntas de quiz.

    Tema: {state["tema"]}
    Dificuldade: {state["dificuldade"]}

    OBJETIVO:

    Gere somente os enunciados das perguntas. As perguntas serão processadas
    posteriormente para gerar embeddings e recuperar o contexto necessário
    para a criação das alternativas, da resposta correta e da explicação.

    FORMATO DE CADA PERGUNTA:

    - Cada pergunta deve possuir somente um enunciado.
    - O enunciado deve ser claro, objetivo e compreensível isoladamente.
    - Não gere alternativas.
    - Não informe a resposta correta.
    - Não gere explicação.
    - Não inclua metadados, comentários ou justificativas.

    DIFICULDADE:

    A dificuldade deve considerar o conhecimento necessário para responder
    à pergunta, e não apenas a complexidade da escrita.

    FÁCIL:
    - Deve ser respondível por uma pessoa comum com conhecimento geral
      sobre o tema.
    - Priorize informações populares, conhecidas e frequentemente associadas
      ao tema.
    - Evite detalhes específicos, técnicos ou pouco conhecidos.
    - Exija principalmente reconhecimento ou lembrança de uma informação.
    - Evite múltiplas etapas de raciocínio.

    MÉDIO:
    - Deve exigir familiaridade com o tema.
    - Pode utilizar informações menos óbvias, mas acessíveis a alguém que
      conheça razoavelmente o assunto.
    - Pode exigir comparação, associação ou uma pequena sequência de raciocínio.
    - Evite conhecimentos excessivamente específicos ou especializados.

    DIFÍCIL:
    - Deve exigir conhecimento aprofundado ou a relação entre informações
      do tema.
    - Pode utilizar detalhes relevantes ou exigir raciocínio em múltiplas
      etapas.
    - Deve continuar sendo justa e respondível.
    - Não utilize uma informação obscura apenas para aumentar a dificuldade.
    - Evite conhecimento profissional altamente especializado, a menos que
      isso seja solicitado.

    IMPOSSÍVEL:
    - Pode exigir conhecimento muito especializado.
    - Pode exigir comparação, associação ou uma sequência de raciocínios
      complexos.
    - Pode utilizar informações desconhecidas por uma pessoa comum.

    MISTA:
    - Combine perguntas fáceis, médias e difíceis.
    - Distribua aproximadamente 20% fáceis, 50% médias e 30% difíceis.
    - Distribua os níveis ao longo do quiz, sem concentrar perguntas de um
      mesmo nível em sequência.
    - Considere a quantidade total ao aproximar os percentuais.

    REGRAS IMPORTANTES:

    - Se a dificuldade não for MISTA, mantenha o nível solicitado em todas as
      perguntas.
    - Priorize perguntas interessantes e relevantes para o tema.
    - Não utilize informações fora do tema solicitado.
    - Não crie perguntas ambíguas.
    - Evite perguntas que possam ter mais de uma resposta razoavelmente correta.
    - Não repita perguntas nem formule a mesma pergunta com palavras diferentes.
    - Não invente fatos.
    """
