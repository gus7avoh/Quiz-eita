# Quiz-eita

Aplicação web para criação e aplicação de quizzes com perguntas geradas pelo Google Gemini. O projeto reúne um frontend Vue/Vite e uma API FastAPI no mesmo repositório. Em produção, o Dockerfile compila o frontend e faz o FastAPI servir a interface e as rotas HTTP pelo mesmo domínio.

## O que é o Quiz-eita?

O Quiz-eita transforma um tema escolhido pelo usuário em um jogo de perguntas. A pessoa informa sobre o que quer ser avaliada, escolhe o nível de dificuldade e espera a inteligência artificial preparar o quiz. Depois responde às perguntas na tela e recebe a quantidade de acertos.

O projeto foi criado para o encontro integrador de tecnologia da Faculdade Anhanguera. Ele combina uma interface web simples para jogar com um serviço que gera as perguntas, guarda o progresso e usa documentos de apoio quando esse conteúdo está disponível.

### Como uma pessoa usa a aplicação

1. A pessoa informa um tema, como `Python`, `cinema` ou `história do Brasil`.
2. Escolhe uma dificuldade: fácil, médio, difícil, impossível ou misto.
3. Clica em **Criar quiz**. A aplicação mostra que a geração está em andamento.
4. Quando as perguntas ficam prontas, a interface apresenta uma pergunta por vez, com suas alternativas.
5. A pessoa pode avançar e voltar entre as perguntas antes de enviar as respostas.
6. Ao terminar, clica para enviar as respostas e vê a quantidade de acertos.
7. Pode voltar ao menu e criar outro quiz.

O fluxo é assíncrono: o servidor cria um identificador imediatamente e prepara as perguntas em segundo plano. Por isso, a tela consulta o servidor algumas vezes enquanto aguarda o resultado.

### O que já está disponível e o que é demonstrativo

- O fluxo de criação, geração, resposta e correção do quiz é o recurso principal e está ligado à API.
- A área de ranking aparece na interface, mas os nomes atuais são fixos no código. Ela ainda não representa pontuações salvas no servidor.
- Há botões de teste de fala e escuta no frontend. O reconhecimento de voz depende do navegador, da permissão do microfone e de HTTPS ou `localhost`; ele ainda funciona como recurso auxiliar de teste.

## Funcionalidades

- criação assíncrona de quizzes por tema, quantidade e dificuldade;
- consulta das perguntas depois que a geração termina;
- correção de respostas e retorno da alternativa correta e da explicação;
- exclusão de um ou vários quizzes;
- geração com contexto documental armazenado no Redis;
- sincronização de documentos do Google Drive para o cache RAG;
- reconhecimento de voz no navegador;
- endpoint de saúde e documentação OpenAPI.

A criação retorna um UUID imediatamente. A geração continua em segundo plano e grava o estado no Redis como `processing`, `completed` ou `failed`.

## Estrutura

```text
Quiz-eita/
├── Dockerfile
├── requirements.txt
├── start.ps1
├── README.md
├── quiz/
│   └── src/
│       ├── app/
│       │   ├── graph/              # fluxo LangGraph da geração
│       │   └── prompts/            # prompts gerais e por tema
│       ├── domain/                 # entidades Pydantic e regras de domínio
│       ├── infra/
│       │   ├── document/           # extração e tratamento de documentos
│       │   ├── llm/                # Gemini, embeddings e gerenciamento de chaves
│       │   └── repository/         # Redis e Google Drive
│       └── presentation/
│           ├── http/               # FastAPI, rotas, schemas e serviços
│           └── cli/
├── interface-quiz/
│   ├── package.json
│   ├── package-lock.json
│   ├── index.html
│   └── src/                        # aplicação Vue/TypeScript
│       ├── components/             # telas e partes visuais do quiz
│       ├── service/                # chamadas HTTP para a API
│       ├── types/                  # tipos das requisições e respostas
│       └── speechRecognitionService.ts
└── venv/                           # ambiente local, não versionado
```

Os manifests Node ficam em `interface-quiz/`. Não há `package.json` nem `package-lock.json` na raiz. O ambiente Python usa `requirements.txt` na raiz.

A aplicação ASGI está em `quiz/src/presentation/http/main.py`, no objeto `app`. O comando precisa apontar `--app-dir .\quiz\src` quando executado a partir da raiz.

## Pré-requisitos

- Python 3.11 ou superior;
- Node.js 22 ou superior para desenvolvimento/build do frontend;
- npm;
- um servidor Redis acessível;
- uma ou mais chaves válidas do Google Gemini;
- credenciais de serviço do Google Drive quando a sincronização documental for usada;
- Docker Desktop, caso queira executar a imagem localmente.

## Configurar o ambiente Python

A partir da raiz do projeto:

```powershell
cd C:\cod\Quiz-eita
py -3.11 -m venv .\venv
.\venv\Scripts\Activate.ps1
```

Se a política do PowerShell impedir a ativação, libere somente a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

Confirme que FastAPI e o servidor ASGI estão instalados na mesma virtualenv usada para iniciar a aplicação:

```powershell
.\venv\Scripts\python.exe -c "import fastapi, uvicorn, redis, langgraph, langchain_google_genai; print('Dependências carregadas com sucesso')"
```

## Configurar variáveis de ambiente

Crie o arquivo `C:\cod\Quiz-eita\.env` somente para o desenvolvimento local. Ele é carregado a partir da raiz do projeto, independentemente do diretório atual do processo.

Exemplo sem credenciais reais:

```dotenv
REDIS_URL=redis://localhost:6379/0
REDIS_URL_RAG=redis://localhost:6379/1

EITA_1=sua-chave-do-gemini-1
EITA_2=sua-chave-do-gemini-2

GOOGLE_DRIVE_FOLDER_ID=id-da-pasta
GOOGLE_DRIVE_CREDENTIALS_NAME=eita-rag-b1b0272909ff.json

# Necessário somente quando o frontend estiver em outra origem
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

Variáveis usadas:

| Variável                        | Finalidade                                                            |
| ------------------------------- | --------------------------------------------------------------------- |
| `REDIS_URL`                     | estados dos quizzes e resultados                                      |
| `REDIS_URL_RAG`                 | documentos, embeddings e contexto RAG                                 |
| `EITA_1` até `EITA_58`          | chaves disponíveis para o Gemini; pelo menos uma é necessária         |
| `GOOGLE_DRIVE_FOLDER_ID`        | pasta de documentos usada na sincronização                            |
| `GOOGLE_DRIVE_CREDENTIALS_NAME` | caminho do JSON da conta de serviço do Google Drive                   |
| `CORS_ORIGINS`                  | origens permitidas quando frontend e API estão em domínios diferentes |

As chaves `EITA_1` até `EITA_58` são opcionais individualmente. Cadastre apenas as que existirem. Nunca publique valores reais no README, no Git ou em logs.

O arquivo de credenciais do Google Drive e os arquivos `.env` estão no `.gitignore`. A variável `GOOGLE_DRIVE_CREDENTIALS_NAME` pode receber um caminho absoluto, como `/run/secrets/google-drive.json` no container, ou um caminho relativo à raiz em ambiente local.

## Iniciar o Redis local

O pacote Python `redis` é apenas o cliente. É preciso executar um servidor Redis.

Com Docker:

```powershell
docker run --name quiz-eita-redis -p 6379:6379 -d redis:7-alpine
```

Se o container já existir:

```powershell
docker start quiz-eita-redis
```

O exemplo usa o banco lógico `0` para os quizzes e o banco `1` para o contexto RAG. É possível usar outra instância ou outros bancos, desde que `REDIS_URL` e `REDIS_URL_RAG` estejam configuradas.

## Executar a API localmente

Com o Redis e o arquivo `.env` configurados, execute a partir de `C:\cod\Quiz-eita`:

```powershell
.\venv\Scripts\python.exe -m uvicorn presentation.http.main:app `
  --app-dir .\quiz\src `
  --host 127.0.0.1 `
  --port 8000 `
  --reload
```

O servidor ficará disponível em:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

O script [start.ps1](start.ps1) executa o mesmo servidor usando automaticamente `venv\Scripts\python.exe` e a pasta `quiz\src`:

```powershell
.\start.ps1
```

Não use `--reload` em produção.

### Verificar a API

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Resposta esperada:

```json
{ "status": "ok" }
```

## Frontend

O frontend fica em `interface-quiz/` e é uma aplicação Vue 3 escrita em TypeScript, com Vite para desenvolvimento e build. Ele cuida da experiência de quem está jogando: coleta o tema e a dificuldade, acompanha a geração, exibe as perguntas e envia as respostas para a API.

### Telas e componentes

| Arquivo                           | Responsabilidade                                                              |
| --------------------------------- | ----------------------------------------------------------------------------- |
| `src/App.vue`                     | ponto de entrada visual; monta a página do quiz e a área de teste de voz      |
| `src/components/FrontPage.vue`    | organiza o título, o ranking lateral e a área principal do jogo               |
| `src/components/SelectGame.vue`   | formulário de tema e dificuldade, criação do quiz e espera pelas perguntas    |
| `src/components/QuizGame.vue`     | exibe uma pergunta por vez, permite voltar ou avançar e envia as respostas    |
| `src/components/RankingBar.vue`   | apresenta a área visual do ranking                                            |
| `src/service/QuizService.ts`      | concentra as chamadas HTTP para criar, consultar, responder e excluir quizzes |
| `src/types/QuizTypes.ts`          | descreve em TypeScript o formato dos dados trocados com a API                 |
| `src/speechRecognitionService.ts` | encapsula fala do navegador e reconhecimento de voz                           |
| `src/testeVoz.vue`                | oferece os botões de teste de fala e escuta                                   |

### O que acontece no frontend

- Ao clicar em **Criar quiz**, `SelectGame.vue` envia tema, dificuldade e a quantidade `5` para `POST /quiz/create`. O nome ainda não existe nessa etapa.
- O servidor devolve um UUID. A tela consulta `POST /quiz/question` a cada dois segundos, por no máximo vinte tentativas.
- Quando as perguntas chegam, `QuizGame.vue` guarda a alternativa marcada para cada pergunta. A navegação permite voltar e corrigir uma escolha antes do envio.
- Ao finalizar, `QuizService.ts` chama `POST /quiz/answer` uma vez para cada pergunta. Cada resposta correta soma um ponto no estado temporário do quiz.
- Depois que o jogador informa o nome, a interface chama `POST /ranking` com `nome`, `pontos` e `dificuldade`. Só então chama `DELETE /quiz` para apagar o quiz que estava aberto e limpa o estado local.

Essa separação ajuda a localizar mudanças: aparência e fluxo de tela ficam em `src/components`, formato dos dados fica em `src/types` e integração com o servidor fica em `src/service`.

### Desenvolvimento do frontend

O frontend tem seus próprios manifests em `interface-quiz/`:

```powershell
cd C:\cod\Quiz-eita\interface-quiz
npm ci
npm run dev
```

Por padrão, o Vite usa a porta `5173`. Para apontar o frontend local para a API local, crie `interface-quiz/.env.local`:

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

Depois abra o endereço exibido pelo Vite, normalmente:

```text
http://localhost:5173
```

O frontend usa `/quiz/create`, `/quiz/question`, `/quiz/answer` e `/quiz`. Em produção no mesmo container, `VITE_API_URL` deve ficar vazio para que o navegador use a mesma origem.

Para gerar os arquivos estáticos:

```powershell
cd C:\cod\Quiz-eita\interface-quiz
npm run build
```

O comando `npm run build` executa a verificação de tipos com `vue-tsc` e depois gera os arquivos finais em `interface-quiz/dist/`. O Dockerfile usa esse mesmo build e copia o resultado para a imagem Python.

Para alterar a interface, edite o componente correspondente, rode `npm run build` e abra a aplicação com `npm run dev` para conferir o resultado. Para alterar o formato de uma chamada, atualize em conjunto o tipo em `src/types/QuizTypes.ts`, o método em `src/service/QuizService.ts` e a rota FastAPI correspondente.

### Onde fazer cada tipo de mudança

| Se você quer...                                          | Comece por...                                                                                 |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| mudar cores, textos ou a disposição da página            | `interface-quiz/src/components/` e os estilos do componente                                   |
| mudar o formulário ou a quantidade de perguntas exibidas | `interface-quiz/src/components/SelectGame.vue`                                                |
| mudar a navegação, alternativas ou resultado             | `interface-quiz/src/components/QuizGame.vue`                                                  |
| alterar uma chamada feita pelo navegador                 | `interface-quiz/src/service/QuizService.ts`                                                   |
| alterar o formato de um request ou response              | `interface-quiz/src/types/QuizTypes.ts` e os schemas em `quiz/src/presentation/http/schemas/` |
| criar ou alterar uma rota                                | `quiz/src/presentation/http/routes/` e o serviço correspondente                               |
| mudar como as perguntas são geradas                      | `quiz/src/app/graph/`, `quiz/src/app/prompts/` e `quiz/src/infra/llm/`                        |
| alterar a imagem publicada                               | `Dockerfile` e as configurações do Dokploy                                                    |

### Configuração da URL da API

`VITE_API_URL` é lida durante o build do frontend:

- vazia ou ausente: usa a mesma origem da página, indicado para o Docker e para produção com um domínio único;
- `http://127.0.0.1:8000`: usa uma API FastAPI iniciada separadamente durante o desenvolvimento;
- outro domínio: exige que a API permita a origem em `CORS_ORIGINS`.

Como as variáveis `VITE_*` entram nos arquivos públicos gerados, nunca coloque chaves secretas nelas. Elas servem apenas para configurações que podem ser conhecidas pelo navegador, como uma URL pública.

O reconhecimento de voz do navegador exige HTTPS ou `localhost`. Por isso, ele funciona no desenvolvimento em `localhost` e no domínio HTTPS configurado em produção.

## Rodar o projeto completo localmente

Para testar a experiência inteira, use três terminais abertos na raiz do projeto:

1. Inicie o Redis com `docker start quiz-eita-redis` ou crie o container conforme a seção de Redis.
2. No segundo terminal, configure o `.env` e execute a API com `.\start.ps1`.
3. No terceiro terminal, execute `cd C:\cod\Quiz-eita\interface-quiz`, `npm ci` (na primeira vez) e `npm run dev`.
4. Abra `http://localhost:5173` e crie um quiz. O navegador usará `VITE_API_URL` para encontrar a API.

O terminal da API precisa permanecer aberto enquanto o frontend estiver sendo usado. Para encerrar o desenvolvimento, pare o servidor com `Ctrl+C`; o Redis pode continuar parado com `docker stop quiz-eita-redis`.

## Contrato da API

### `GET /health`

Verifica se o processo FastAPI está ativo.

Resposta:

```json
{ "status": "ok" }
```

### `POST /quiz/create`

Inicia a geração e retorna o UUID.

Request:

```json
{
  "tema": "python",
  "quantidade": 5,
  "dificuldade": "mista"
}
```

Resposta:

```json
{ "uuid": "codigo-gerado" }
```

`tema` e `dificuldade` devem ser textos não vazios. `quantidade` deve ser maior que zero. Requests inválidos retornam `422`.

### `POST /ranking`

Registra o resultado depois que o jogador termina a partida:

```json
{
  "nome": "Ana",
  "pontos": 4,
  "dificuldade": "Fácil"
}
```

O nome não participa da criação do quiz. O ranking é persistido por dificuldade e a resposta indica se o registro foi adicionado:

```json
{ "added": true }
```

### `POST /quiz/question`

Consulta as perguntas de um quiz:

```json
{
  "uuid": "codigo-gerado"
}
```

Quando o quiz está concluído:

```json
{
  "perguntas": [
    {
      "enunciado": "Qual estrutura é usada para criar uma lista em Python?",
      "alternativas": ["[]", "{}", "()", "<>"]
    }
  ]
}
```

Enquanto o quiz estiver em `processing` ou não existir, a rota retorna `null`. Se a geração tiver falhado, retorna HTTP `500`. As alternativas podem ser embaralhadas antes da resposta.

### `POST /quiz/answer`

Corrige uma resposta pelo texto do enunciado:

```json
{
  "uuid": "codigo-gerado",
  "enunciado": "Qual estrutura é usada para criar uma lista em Python?",
  "resposta_usuario": "[]"
}
```

Resposta:

```json
{
  "resposta": {
    "resposta": "[]",
    "correta": true,
    "explicacao": "Colchetes criam listas em Python."
  }
}
```

A resposta é `null` enquanto o quiz estiver em processamento, não existir ou quando o enunciado não for encontrado. Se a geração tiver falhado, retorna HTTP `500`.

### `DELETE /quiz`

Exclui um ou mais quizzes. O corpo da requisição é:

```json
{
  "list_uuid": [{ "uuid": "codigo-gerado" }, { "uuid": "outro-codigo" }]
}
```

Resposta:

```json
{ "excluded": true }
```

## Estados e armazenamento no Redis

Cada quiz usa a chave `quiz:<uuid>`:

- `processing`: UUID criado e geração em andamento;
- `completed`: perguntas geradas e salvas no campo `quiz`;
- `failed`: ocorreu erro e o campo `error` registra a falha.

Para inspeção local, prefira `SCAN` a `KEYS`:

```powershell
docker exec quiz-eita-redis redis-cli -n 0 SCAN 0 MATCH "quiz:*" COUNT 100
```

O contexto documental usa `REDIS_URL_RAG`. Mantenha o banco RAG separado do banco dos quizzes quando a instância Redis for compartilhada.

Os clientes de quiz e RAG fazem até duas tentativas por operação Redis (a inicial e uma repetição), sem espera adicional entre elas, em falhas de conexão ou timeout. Os timeouts de conexão e de leitura são de 5 segundos cada. A política também se aplica aos comandos de `SCAN`/`SSCAN` e aos pipelines.

Se ambas as tentativas falharem durante uma requisição, a API retorna HTTP `500` com `{"detail":"Falha ao acessar o Redis. Tente novamente."}`. A geração do quiz ocorre em segundo plano: falhas posteriores à criação são registradas como `failed`, quando o Redis permite gravar esse estado, e as consultas de perguntas e respostas retornam HTTP `500` ao encontrá-lo.

## Contexto documental e Google Drive

O grafo de geração executa estas etapas:

1. inicia ou mantém o processo de sincronização do Google Drive;
2. procura no Redis RAG o contexto relacionado ao tema;
3. gera as perguntas com o Gemini usando esse contexto;
4. salva o quiz no Redis principal.

Para a sincronização, a conta de serviço precisa ter acesso de leitura à pasta indicada por `GOOGLE_DRIVE_FOLDER_ID`. O JSON da conta de serviço não deve ser copiado para a imagem Docker nem enviado ao repositório.

## Testes e validações locais

O repositório não possui uma suíte automatizada completa. Execute pelo menos estas verificações antes de publicar:

```powershell
cd C:\cod\Quiz-eita

.\venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'quiz/src'); from presentation.http.main import app; print(app.title)"

.\venv\Scripts\python.exe -m unittest discover -s quiz/tests -v

cd .\interface-quiz
npm ci
npm run build
```

Os testes de retry exercitam a política da biblioteca Redis e as rotas FastAPI com falhas simuladas, sem conectar a um servidor Redis.

Com Redis, as variáveis e as credenciais configuradas, valide também `/health` e o fluxo das rotas descritas acima. A importação, os testes isolados e o build não comprovam conectividade com Redis, Gemini ou Google Drive.

## Deploy com Docker

O [Dockerfile](Dockerfile) usa duas etapas:

1. a imagem Node 22 instala as dependências de `interface-quiz` e executa `npm run build`;
2. a imagem Python 3.11 instala `requirements.txt`, copia a API e serve o frontend compilado pelo FastAPI.

A imagem final expõe a porta `8000` e inicia:

```text
uvicorn presentation.http.main:app --app-dir /app/quiz/src --host 0.0.0.0 --port 8000
```

Teste localmente, com Docker Desktop ativo:

```powershell
docker build -t quiz-eita:local .

docker run --rm -p 8000:8000 `
  -e REDIS_URL="redis://host.docker.internal:6379/0" `
  -e REDIS_URL_RAG="redis://host.docker.internal:6379/1" `
  -e EITA_1="sua-chave-do-gemini" `
  quiz-eita:local
```

Abra:

```text
http://localhost:8000/
http://localhost:8000/health
```

O arquivo `.env` da raiz não é copiado para a imagem. Em um servidor, forneça as variáveis pelo ambiente do container ou pelo recurso de secrets do provedor.

## Deploy no Dokploy

Na aplicação do Dokploy, use:

| Campo              | Valor                            |
| ------------------ | -------------------------------- |
| Origem             | repositório GitHub `Quiz-eita`   |
| Branch             | `main`                           |
| Build Type         | `Dockerfile`                     |
| Dockerfile         | `Dockerfile`                     |
| Context Path       | `.` ou `/`, conforme a interface |
| Stage              | `production`                     |
| Porta do container | `8000`                           |

Cadastre os segredos e variáveis no ambiente do Dokploy. Não dependa do `.env` local:

```dotenv
REDIS_URL=redis://usuario:senha@host:6379/0
REDIS_URL_RAG=redis://usuario:senha@host:6379/1
EITA_1=sua-chave-do-gemini-1
EITA_2=sua-chave-do-gemini-2
GOOGLE_DRIVE_FOLDER_ID=id-da-pasta
GOOGLE_DRIVE_CREDENTIALS_NAME=/run/secrets/google-drive.json
```

Se o frontend e a API usarem o mesmo domínio, não defina `VITE_API_URL`. Se forem domínios diferentes, `VITE_API_URL` precisa estar disponível durante o build do frontend e `CORS_ORIGINS` precisa conter a origem pública do frontend.

### Domínio e HTTPS

Para o domínio atual `quiz-eita.com.br`, o registro DNS deve apontar para o IP público do servidor:

```text
Tipo: A
Nome: @ ou vazio
Valor: 169.58.5.68
```

Opcionalmente, crie também:

```text
Tipo: CNAME
Nome: www
Valor: quiz-eita.com.br
```

No domínio do Dokploy, use:

| Campo                | Valor              |
| -------------------- | ------------------ |
| Host                 | `quiz-eita.com.br` |
| Path                 | `/`                |
| Internal Path        | `/`                |
| Strip Path           | desligado          |
| Container Port       | `8000`             |
| Custom Entrypoint    | desligado          |
| HTTPS                | ligado             |
| Certificate Provider | Let's Encrypt      |

Não use o endereço `sslip.io` para o certificado. Ele é útil para apontamento HTTP, mas não oferece SSL/HTTPS próprio.

Antes de solicitar o certificado, confirme:

```powershell
Resolve-DnsName quiz-eita.com.br -Type A
```

O domínio precisa retornar `169.58.5.68`. As portas públicas `80` e `443` também precisam estar acessíveis no servidor para o proxy e o desafio do Let's Encrypt.

Depois do deploy:

```text
https://quiz-eita.com.br/health
https://quiz-eita.com.br/
https://quiz-eita.com.br/docs
```

A rota `/health` comprova que o processo FastAPI está ativo. A criação de quizzes também depende de Redis, chaves Gemini e, quando usado, Google Drive e Redis RAG.

## Solução de problemas

### FastAPI não é reconhecido

Use o interpretador da virtualenv explicitamente:

```powershell
.\venv\Scripts\python.exe -m pip show fastapi
.\venv\Scripts\python.exe -c "import fastapi; print(fastapi.__version__)"
```

O `python` global pode apontar para outra instalação sem FastAPI. O Docker instala as dependências a partir de `requirements.txt` dentro da imagem.

### Erro `No module named presentation`

Execute a partir da raiz e inclua o diretório da aplicação:

```powershell
.\venv\Scripts\python.exe -m uvicorn presentation.http.main:app --app-dir .\quiz\src
```

### `REDIS_URL não foi configurada`

Confirme que a variável existe no ambiente do processo. No Dokploy, cadastre-a nas variáveis da aplicação; o `.env` da sua máquina não é enviado para o container.

### O quiz permanece em `processing`

Verifique os logs do Uvicorn/Dokploy, a conectividade com `REDIS_URL` e `REDIS_URL_RAG`, a existência de ao menos uma chave `EITA_*` e o processo de sincronização documental.

### O domínio abre, mas o HTTPS não é emitido

Confirme que:

- o domínio retorna o IP correto em uma consulta DNS pública;
- o host no Dokploy é o domínio real, sem `http://` e sem `:8000`;
- a porta interna está como `8000`;
- as portas públicas `80` e `443` estão liberadas;
- o provedor de certificado está definido como `Let's Encrypt`.

### O microfone não funciona

O navegador exige contexto seguro para o microfone. Use `localhost` no desenvolvimento ou o domínio HTTPS em produção. Verifique também a permissão de microfone do navegador.

## Segurança e operação

- não versione `.env`, credenciais do Google Drive, certificados ou chaves privadas;
- não coloque senhas, URLs Redis ou chaves Gemini em logs;
- use Redis autenticado e protegido por rede em produção;
- mantenha `--reload` desligado em produção;
- configure o Dokploy ou outro supervisor para reiniciar o container;
- após uma alteração de DNS, valide o domínio e o certificado antes de divulgar a URL.
