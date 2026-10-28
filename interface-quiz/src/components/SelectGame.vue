<script lang="ts" setup>
  import { ref } from 'vue'
  import { criarQuiz, buscarQuiz, deletarQuiz, adicionarUsuario, comecarMusica, mudarVolumeMusica } from '../service/QuizService'
  import type { BuscarQuizResponse, Configuracoes, DeletarRequest, Usuario } from '../types/QuizTypes'
  import QuizGame from './QuizGame.vue'
  import ConfiguracoesJogo from './ConfiguracoesJogo.vue'

  const emit = defineEmits<{
    (event: 'quiz-ativo', ativo: boolean): void
  }>()

  const tema = ref('')
  const temaPredefinido = ref('')
  const dificuldade = ref('')
  const uuid = ref('')
  const quiz = ref<BuscarQuizResponse | null> (null)
  const carregando = ref(false)
  const erro = ref('')
  const configuracoes = ref<Configuracoes>({
    botao_acessibilidade: false,
    botao_fala: false,
    botao_voz: false,
    botao_musica: true,
  })
  const volumeMusica = ref(1)
  const ultimoVolumeMusica = ref(1)
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

      const temaSelecionado = temaPredefinido.value || tema.value.trim()
      const id = await criarQuiz({tema: temaSelecionado, quantidade: 5, dificuldade: dificuldade.value})
      uuid.value=id
      await esperarResposta(id)
      if (configuracoes.value.botao_musica) {
        comecarMusica(dificuldade.value)
        mudarVolumeMusica(volumeMusica.value)
      }
      if (quiz.value) emit('quiz-ativo', true)

    }

    catch(e) {
      console.log(e)
      erro.value = 'Erro ao gerar quiz, tente novamente'
    }

    finally{
      carregando.value = false
    }

  }

  function alternarFala() {
    configuracoes.value.botao_fala = !configuracoes.value.botao_fala
  }

  function alternarVoz() {
    configuracoes.value.botao_voz = !configuracoes.value.botao_voz
  }

  function alternarMusica() {
    if (configuracoes.value.botao_musica) {
      configuracoes.value.botao_musica = false
      mudarVolumeMusica(0)
      return
    }

    const volumeRestaurado = ultimoVolumeMusica.value > 0 ? ultimoVolumeMusica.value : 1
    configuracoes.value.botao_musica = true
    volumeMusica.value = volumeRestaurado
    mudarVolumeMusica(volumeRestaurado)
  }

  function alterarVolumeMusica(volume: number) {
    const volumeLimitado = Math.max(0, Math.min(1, volume))
    volumeMusica.value = volumeLimitado
    mudarVolumeMusica(volumeLimitado)

    if (volumeLimitado === 0) {
      configuracoes.value.botao_musica = false
      return
    }

    ultimoVolumeMusica.value = volumeLimitado
    configuracoes.value.botao_musica = true
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
      emit('quiz-ativo', false)
      uuid.value = ''
      tema.value = ''
      temaPredefinido.value = ''
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
    emit('quiz-ativo', false)
    uuid.value=''
    tema.value=''
    temaPredefinido.value = ''
    dificuldade.value=''

  }



</script>

<template>
  <ConfiguracoesJogo
    :musica-ativa="configuracoes.botao_musica"
    :voz-ativa="configuracoes.botao_voz"
    :fala-ativa="configuracoes.botao_fala"
    :volume-musica="volumeMusica"
    @alternar-musica="alternarMusica"
    @alternar-voz="alternarVoz"
    @alternar-fala="alternarFala"
    @volume-change="alterarVolumeMusica"
  />

  <div id="janela">

    <header class="sr-only">

        <h1>Jogo</h1>

    </header>

    <main class="stage">

      <div v-if = "!quiz" class="setup">

        <h2 class="setup-title">Monte seu quiz</h2>

        <div class="field">
          <label for="tema">Tema do quiz</label>
          <div class="theme-fields">
            <input id="tema" class="text-input" v-model="tema" @input="digitarTema" placeholder="Ex.: Vue, redes, banco de dados"/>

            <label for="tema-predefinido">Ou escolha um tema</label>
            <select id="tema-predefinido" class="select-input" v-model="temaPredefinido" @change="selecionarTemaPredefinido">
              <option value=""></option>
              <option v-for="temaOpcao in temasPredefinidos" :key="temaOpcao" :value="temaOpcao">
                {{ temaOpcao }}
              </option>
            </select>
          </div>
        </div>

        <fieldset class="field">

          <legend>Selecione uma dificuldade</legend>

          <div class="chips">

            <label class="chip">
              <input type="radio" name="dificuldade" value="Fácil" v-model="dificuldade"/>
              <span class="chip-body"><span class="dot dot-facil"></span>Fácil</span>
            </label>

            <label class="chip">
              <input type="radio" name="dificuldade" value="Médio" v-model="dificuldade"/>
              <span class="chip-body"><span class="dot dot-medio"></span>Médio</span>
            </label>

            <label class="chip">
              <input type="radio" name="dificuldade" value="Difícil" v-model="dificuldade"/>
              <span class="chip-body"><span class="dot dot-dificil"></span>Difícil</span>
            </label>

            <label class="chip">
              <input type="radio" name="dificuldade" value="Impossível" v-model="dificuldade"/>
              <span class="chip-body"><span class="dot dot-impossivel"></span>Impossível</span>
            </label>

            <label class="chip">
              <input type="radio" name="dificuldade" value="Misto" v-model="dificuldade"/>
              <span class="chip-body"><span class="dot dot-misto"></span>Misto</span>
            </label>

          </div>

        </fieldset>

        <div class="actions">

          <button class="btn" :class="{ loading: carregando }" :disabled="carregando || (!tema.trim() && !temaPredefinido) || !dificuldade" @click="gerarQuiz">
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
        :configuracoes="configuracoes"
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
