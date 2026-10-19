<script lang="ts" setup>

    import { ref, computed } from 'vue'
    import { responderQuiz } from '../service/QuizService';
    import { EnumQuizGame } from '../types/QuizTypes'
    import type { Pergunta, RespostaRequest, Usuario,  EstadoQuiz, RespostaResponse} from '../types/QuizTypes'
    //Pergunta = { enunciado: string, alternativas: string[] }
    //RespostaRequest = { uuid: string, respostas: Resposta[] }
    //Resposta = { enunciado: string, resposta: string }

    //props que vem do SelectGame
const props = defineProps < { 
    perguntas: Pergunta[] 
    uuid: string
    dificuldade: string
    } > ()

const emit = defineEmits< { (e: 'voltarMenu', usuario: Usuario): void } > ()

const estadoQuiz = ref<EstadoQuiz>(EnumQuizGame.respondendo)
const respostaResponse = ref<RespostaResponse | null>(null)
const indice = ref(0)
//muda a pergunta atual automaticamente conforme indice muda
const perguntaAtual = computed( () => props.perguntas[indice.value] ) 
const alternativaSelecionada = ref<string | null> (null) 
const acertos = ref<number>(0)
const nomeUsuario = ref('')
const erro = ref('')


async function enviarResposta() {

    const respostaRequest: RespostaRequest = ({uuid: props.uuid, 'enunciado': perguntaAtual.value.enunciado, 'resposta_usuario': alternativaSelecionada.value!})

    try {
        respostaResponse.value = await responderQuiz(respostaRequest)
        if(respostaResponse.value.correta) {
            acertos.value++
        }
    }
    catch(e) {
        console.error(e)
        erro.value='Houve um erro ao responder o quiz, tente novamente'
        }
    
}

function proximaQuestao() {
    
    if(indice.value < props.perguntas.length - 1) {
        indice.value++
        alternativaSelecionada.value = null
        respostaResponse.value = null
    }
    else {
        estadoQuiz.value = EnumQuizGame.resultado
    }
}

</script>

<template>
    <div v-if="estadoQuiz === 'RESPONDENDO'">
        <p>Pergunta {{ indice+1 }} de {{ perguntas.length }}</p>
    
        <fieldset>

            <legend>{{ perguntaAtual.enunciado }}</legend>
            
            <label v-for="alternativa in perguntaAtual.alternativas" :key="alternativa">

                <input
                type="radio"
                name="alternativa"
                :value="alternativa"
                v-model="alternativaSelecionada"
                />
                {{ alternativa }}

            </label>

            <button :disabled="!alternativaSelecionada" @click="enviarResposta">Responder</button>
            <p v-if="erro">{{ erro }}</p>

        </fieldset>

        <div v-if="respostaResponse">

            <div v-if="respostaResponse.correta===true">
                <p>Você acertou!</p>
            </div>

            <div v-else>
                <p>Você errou!</p>
            </div>

            <p>Explicação: {{ respostaResponse.explicacao }}</p>
            <button @click="proximaQuestao">Próxima</button>
        </div>

        
    </div>

    <div v-else-if="estadoQuiz === 'RESULTADO'">
        <p>Você terminou o quiz!</p>
        <p>Quantidade de acertos: {{ acertos }}</p>
        <input v-model="nomeUsuario" placeholder="Digite seu nome para o ranking"/>
        <button :disabled="!nomeUsuario.trim()" @click="emit('voltarMenu', {nome: nomeUsuario, pontos: acertos})">
            Enviar e voltar para menu
        </button>
    </div>
 
</template>

<style scoped>


</style>