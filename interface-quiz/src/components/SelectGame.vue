<script lang="ts" setup>
  import { ref } from 'vue'
  import { criarQuiz, buscarQuiz, deletarQuiz } from '../service/QuizService'
  import type { BuscarQuizResponse, DeletarRequest } from '../types/QuizTypes'
  import QuizGame from './QuizGame.vue'

  const tema = ref('')
  const playerName = ref('')
  const dificuldade = ref('')
  const uuid = ref('')
  const quiz = ref<BuscarQuizResponse | null> (null)
  const carregando = ref(false)
  const erro = ref('')
  
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

  async function voltarMenu() {

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

    <header>

        <h1>Jogo</h1>

    </header>

    <main>

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

        <p v-if="erro">
          {{ erro }}
        </p>

      </div>
      
      <QuizGame v-else 
        :perguntas="quiz.perguntas"
        :uuid='uuid'
        @voltar-menu="voltarMenu"
      />

    </main>

  </div> <!--div id janela-->
    
</template>

<style scoped>


#janela{
  background-color: #444;
  display: flex;
  flex-direction: column;
  flex:1;
  height: 100%;
  width: 100%;
  border-radius: 12px;
}

header{
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 1.01rem;
    font-family: 'Rubik Marker Hatch', cursive;
    font-weight: normal;
    color: var(--primary-color);
    margin: 0 0 20px 0;
}

.input {
  width: 100%;
  max-width: 270px;
  height: 60px;
  padding: 12px;
  font-size: 18px;
  font-family: "Courier New", monospace;
  color: #000;
  background-color: #fff;
  border: 4px solid #000;
  border-radius: 0;
  outline: none;
  transition: all 0.3s ease;
  box-shadow: 8px 8px 0 #000;
}

.input::placeholder {
  color: #888;
}

.input:hover {
  transform: translate(-4px, -4px);
  box-shadow: 12px 12px 0 #000;
}

.input:focus {
  background-color: #000;
  color: #fff;
  border-color: #ffffff;
}

.input:focus::placeholder {
  color: #fff;
}

@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

@keyframes blink {
  50% {
    border-color: transparent;
  }
}

.input:focus::after {
  content: "|";
  position: absolute;
  right: 10px;
  animation: blink 0.7s step-end infinite;
}

.input:valid {
  animation: typing 2s steps(30, end);
}
.input-container {
  position: relative;
  width: 100%;
  max-width: 270px;
}

.input {
  width: 100%;
  height: 60px;
  padding: 12px;
  font-size: 18px;
  font-family: "Courier New", monospace;
  color: #000;
  background-color: #fff;
  border: 4px solid #000;
  border-radius: 0;
  outline: none;
  transition: all 0.3s ease;
  box-shadow: 8px 8px 0 #000;
}

.input::placeholder {
  color: #888;
}

.input:hover {
  transform: translate(-4px, -4px);
  box-shadow: 12px 12px 0 #000;
}

.input:focus {
  background-color: #010101;
  color: #fff;
  border-color: #d6d9dd;
}

.input:focus::placeholder {
  color: #fff;
}

@keyframes shake {
  0% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px) rotate(-5deg);
  }
  50% {
    transform: translateX(5px) rotate(5deg);
  }
  75% {
    transform: translateX(-5px) rotate(-5deg);
  }
  100% {
    transform: translateX(0);
  }
}

.input:focus {
  animation: shake 0.5s ease-in-out;
}

@keyframes glitch {
  0% {
    transform: none;
    opacity: 1;
  }
  7% {
    transform: skew(-0.5deg, -0.9deg);
    opacity: 0.75;
  }
  10% {
    transform: none;
    opacity: 1;
  }
  27% {
    transform: none;
    opacity: 1;
  }
  30% {
    transform: skew(0.8deg, -0.1deg);
    opacity: 0.75;
  }
  35% {
    transform: none;
    opacity: 1;
  }
  52% {
    transform: none;
    opacity: 1;
  }
  55% {
    transform: skew(-1deg, 0.2deg);
    opacity: 0.75;
  }
  50% {
    transform: none;
    opacity: 1;
  }
  72% {
    transform: none;
    opacity: 1;
  }
  75% {
    transform: skew(0.4deg, 1deg);
    opacity: 0.75;
  }
  80% {
    transform: none;
    opacity: 1;
  }
  100% {
    transform: none;
    opacity: 1;
  }
}

.input:not(:placeholder-shown) {
  animation: glitch 1s linear infinite;
}

.input-container::after {
  content: "|";
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #000;
  animation: blink 0.7s step-end infinite;
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}

.input:focus + .input-container::after {
  color: #fff;
}

.input:not(:placeholder-shown) {
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 0px 0px 0 #000;
}


</style>