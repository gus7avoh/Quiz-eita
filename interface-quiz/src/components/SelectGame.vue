<script lang="ts" setup>
  import { ref } from 'vue'
  import { criarQuiz, buscarQuiz, deletarQuiz, adicionarUsuario } from '../service/QuizService'
  import type { BuscarQuizResponse, DeletarRequest, Usuario } from '../types/QuizTypes'
  import QuizGame from './QuizGame.vue'

  const tema = ref('')
  const playerName = ref('')
  const dificuldade = ref('')
  const uuid = ref('')
  const quiz = ref<BuscarQuizResponse | null> (null)
  const carregando = ref(false)
  const erro = ref('')
  const temasPredefinidos = [
    'c#',
    'famosos',
    'filmes',
    'java',
    'java script',
    'jogos',
    'musicas',
    'python',
  ]

  function selecionarTemaPredefinido() {
    if (temaPredefinido.value) {
      tema.value = ''
    }
  }

  function digitarTema() {
    temaPredefinido.value = ''
  }
  
    //função de criar quiz que chama criarQuiz do QuizService
  async function gerarQuiz() {

    carregando.value = true
    erro.value=''

    try {

      const id = await criarQuiz({
        tema: tema.value.trim(),
        quantidade: 5,
        dificuldade: dificuldade.value,
        player_name: playerName.value.trim(),
      })
      uuid.value=id
      await esperarResposta(id)

    }

    catch(e) {
      console.log(e)
      erro.value = 'Erro ao gerar quiz, tente novamente'
    }

    finally{
      carregando.value = false
    }

  }

    //função de pegar respostas que chama buscarQuiz do QuizService
  async function esperarResposta(id: string) {

      for(let i=0; i<20; i++) { //tenta chamar buscarQuiz 20 vezes
        const resultado = await buscarQuiz(id)

        if(resultado) {
          quiz.value=resultado
          return
        }

        //espera 2 segundos antes de tentar de novo
        if(i<19) await new Promise(resolve => setTimeout(resolve, 2000))
      }

  }

  async function voltarMenu(usuario: Usuario) {
    try{
      const resultado = await adicionarUsuario(usuario.nome, usuario.pontos, dificuldade.value)
      console.log(resultado ? 'usuario adicionado com sucesso' : 'usuario não foi adicionado')
    }
    catch(e) {
      console.error('Erro ao adicionar usuario', e)
    }
    
    if (!uuid.value) {
      quiz.value = null
      uuid.value = ''
      tema.value = ''
      playerName.value = ''
      dificuldade.value = ''
      return
    }

    const quizes: DeletarRequest = { list_uuid: [{uuid: uuid.value}] }

    try{
      const resultado = await deletarQuiz(quizes)
      console.log(resultado ? 'quiz deletado com sucesso' : 'quiz não foi deletado')
    }
    catch(e) {console.error('Erro ao deletar quiz', e)}
    

    quiz.value=null
    uuid.value=''
    tema.value=''
    playerName.value=''
    dificuldade.value=''

  }



</script>

<template>
  <div id="janela">

    <header class="sr-only">

        <h1>Jogo</h1>

    </header>

    <main class="stage">

      <div v-if = "!quiz">
        
        <input v-model="playerName" placeholder="Nome do jogador"/>
        <input v-model="tema" placeholder="Tema do quiz"/>

        <label for="dificuldade">Selecione uma dificuldade</label>        
        <select v-model="dificuldade" id="dificuldade">

          <option disabled value="">Escolha...</option>
          <option value="Fácil">Fácil</option>
          <option value="Médio">Médio</option>
          <option value="Difícil">Difícil</option>
          <option value="Impossível">Impossível</option>
          <option value="Misto">Misto</option>

        </select>
        

        <button :disabled="carregando || !playerName.trim() || !tema.trim() || !dificuldade" @click="gerarQuiz">
          {{carregando ? 'Gerando...' : 'Criar quiz'}}
        </button>

          <p v-if="erro" class="error-msg" role="alert">
            {{ erro }}
          </p>

        </div>

      </div>
      
      <QuizGame v-else 
        :perguntas="quiz.perguntas"
        :uuid='uuid'
        :dificuldade="dificuldade"
        @voltar-menu= "voltarMenu"
      />

    </main>

  </div> <!--div id janela-->
    
</template>

<style scoped>

#janela {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  min-height: 0;
  padding: clamp(16px, 2.5vw, 32px);
  background: var(--paper);
  color: var(--ink);
  border-radius: var(--radius-lg);
  scrollbar-color: var(--cobalt) transparent;
}

.stage {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

/* formulário de criação */
.setup {
  display: flex;
  flex-direction: column;
  gap: clamp(12px, 2vh, 22px);
  width: 100%;
  max-width: 34rem;
  margin: auto;
}

.setup-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 1.1rem + 1.8vw, 2.4rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.field {
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.theme-fields {
  display: grid;
  gap: 12px;
}

.field label,
.field legend {
  display: block;
  margin: 0 0 10px;
  padding: 0;
  font-size: 1rem;
  font-weight: 800;
}

.theme-fields label {
  margin: 2px 0 -4px;
  font-size: 0.95rem;
}

.select-input {
  width: 100%;
  height: 56px;
  padding: 0 18px;
  border: 2px solid var(--line);
  border-radius: 16px;
  background: #fff;
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.select-input:focus {
  outline: none;
  border-color: var(--cobalt);
  box-shadow: 0 0 0 4px rgba(47, 63, 224, 0.2);
}

/* chips de dificuldade */
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.field .chip {
  position: relative;
  display: block;
  margin: 0;
  cursor: pointer;
}

/* o radio fica por cima, invisível, para continuar clicável e focável */
.chip input {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  opacity: 0;
  cursor: pointer;
}

.chip-body {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  height: 48px;
  padding: 0 18px;
  border: 2px solid var(--line);
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 4px 0 var(--line);
  font-weight: 700;
  transition: transform 0.1s ease, box-shadow 0.1s ease, border-color 0.15s ease, background-color 0.15s ease;
}

.chip:hover .chip-body {
  border-color: #B5BAE8;
  box-shadow: 0 4px 0 #B5BAE8;
}

.chip:active .chip-body {
  transform: translateY(3px);
  box-shadow: 0 1px 0 var(--line);
}

.chip input:focus-visible + .chip-body {
  outline: 3px solid var(--cobalt);
  outline-offset: 3px;
}

.chip input:checked + .chip-body {
  border-color: var(--cobalt);
  background: #EEF0FF;
  box-shadow: 0 4px 0 var(--cobalt);
  color: var(--cobalt);
}

.actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
}

/* indicador de carregamento dentro do botão */
.btn.loading::before {
  content: '';
  width: 18px;
  height: 18px;
  border: 3px solid rgba(20, 18, 59, 0.25);
  border-top-color: var(--ink);
  border-radius: 50%;
  animation: girar 0.7s linear infinite;
}

.btn.loading:disabled {
  background: var(--sun);
  color: var(--ink);
  box-shadow: 0 5px 0 var(--sun-edge);
  cursor: progress;
}

@keyframes girar {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 30rem) {
  .actions .btn {
    width: 100%;
  }
}

</style>