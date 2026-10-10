<script lang="ts" setup>
  import { ref } from 'vue'
  import { criarQuiz, buscarQuiz } from '../service/QuizService'
  import type { BuscarQuizResponse } from '../types/QuizTypes'

  const tema = ref('')
  const uuid = ref<string | null> (null)
  const perguntas = ref<BuscarQuizResponse | null> (null)
  
    //função de criar quiz que chama criarQuiz do QuizService
  async function gerarQuiz() {

    try {

      const id = await criarQuiz({tema: tema.value, quantidade: 5, dificuldade: 'misto'}) 
      uuid.value=id
      await esperarResposta(id)

    }
    catch(e) {console.error(e)}
  }

    //função de pegar respostas que chama buscarQuiz do QuizService
  async function esperarResposta(id: string) {
    
      for(let i=0; i<20; i++) { //tenta chamar buscarQuiz 20 vezes
        const resultado = await buscarQuiz(id)

        if(resultado) {
          perguntas.value=resultado
          return
        }

        //espera 2 segundos antes de tentar de novo
        if(i<19) await new Promise(resolve => setTimeout(resolve, 2000))
      }
    console.error('Quiz demorou demais ou falhou')
  }



</script>

<template>
  <div id="janela">

    <h1>ESTOU AQUI</h1>
    <input v-model="tema" placeholder="Tema do quiz"/>
    <button @click="gerarQuiz">Criar quiz</button>

    <div v-if="perguntas">

        <div v-for="(pergunta, index) in perguntas.perguntas":key="index">
          <h3>{{ pergunta.enunciado }}</h3>
          <ul>

            <li v-for="(alternativa, i) in pergunta.alternativas">

                {{ alternativa }}

            </li>

          </ul>

        </div>

    </div>
    
  </div>
    
</template>

<style scoped>


#janela{
  background-color: white;
  display: flex;
  flex:1;
  height: 100%;
  width: 100%;
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