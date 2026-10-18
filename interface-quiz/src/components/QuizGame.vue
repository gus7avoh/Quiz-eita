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
    <div v-if="estadoQuiz === 'RESPONDENDO'" class="quiz">

        <div class="progress">
            <p class="progress-label">Pergunta {{ indice+1 }} de {{ perguntas.length }}</p>

            <div class="progress-bar" aria-hidden="true">
                <span
                    v-for="n in perguntas.length"
                    :key="n"
                    class="seg"
                    :class="{ done: n - 1 < indice, current: n - 1 === indice }"
                ></span>
            </div>
        </div>
    
        <fieldset class="question">

            <legend>{{ perguntaAtual.enunciado }}</legend>

            <div class="options">

                <label v-for="(alternativa, i) in perguntaAtual.alternativas" :key="alternativa" class="option">

                    <input
                    type="radio"
                    name="alternativa"
                    :value="alternativa"
                    v-model="alternativaSelecionada"
                    />

                    <span
                        class="option-body"
                        :class="{
                            correct: respostaResponse && alternativaSelecionada === alternativa && respostaResponse.correta,
                            wrong: respostaResponse && alternativaSelecionada === alternativa && !respostaResponse.correta
                        }"
                    >
                        <span class="option-key">{{ 'ABCDEFGH'[i] }}</span>
                        <span class="option-text">{{ alternativa }}</span>
                    </span>

                </label>

            </div>

            <div class="actions">
                <button class="btn" :disabled="!alternativaSelecionada" @click="enviarResposta">Responder</button>
                <p v-if="erro" class="error-msg" role="alert">{{ erro }}</p>
            </div>

        </fieldset>

        <div
            v-if="respostaResponse"
            class="feedback"
            :class="respostaResponse.correta === true ? 'is-correct' : 'is-wrong'"
            role="status"
        >

            <span class="feedback-icon" aria-hidden="true">
                <svg v-if="respostaResponse.correta === true" viewBox="0 0 24 24" width="24" height="24">
                    <path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" width="24" height="24">
                    <path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
                </svg>
            </span>

            <div class="feedback-body">

                <div v-if="respostaResponse.correta===true">
                    <p class="feedback-title">Você acertou!</p>
                </div>

                <div v-else>
                    <p class="feedback-title">Você errou!</p>
                </div>

                <p class="explanation">Explicação: {{ respostaResponse.explicacao }}</p>

            </div>

            <button class="btn" @click="proximaQuestao">Próxima</button>

        </div>

        
    </div>

    <div v-else-if="estadoQuiz === 'RESULTADO'" class="result">

        <p class="result-title">Você terminou o quiz!</p>

        <div class="score">
            <p class="score-value">
                <span class="score-number">{{ acertos }}</span>
                <span class="score-total">/ {{ perguntas.length }}</span>
            </p>
            <p class="score-label">Quantidade de acertos</p>
        </div>

        <div class="save">
            <input class="text-input" v-model="nomeUsuario" placeholder="Digite seu nome para o ranking" aria-label="Seu nome para o ranking"/>
            <button class="btn" :disabled="!nomeUsuario.trim()" @click="emit('voltarMenu', {nome: nomeUsuario, pontos: acertos})">
                Enviar e voltar para menu
            </button>
        </div>

    </div>
 
</template>

<style scoped>

.quiz {
    width: 100%;
    max-width: 54rem;
    margin: 0 auto;
}

/* progresso */
.progress {
    margin-bottom: 28px;
}

.progress-label {
    margin: 0 0 10px;
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 700;
}

.progress-bar {
    display: flex;
    gap: 6px;
}

.seg {
    flex: 1;
    height: 8px;
    border-radius: 99px;
    background: #DDE0F5;
    transition: background-color 0.2s ease;
}

.seg.done {
    background: var(--cobalt);
}

.seg.current {
    background: var(--sun);
}

/* pergunta */
.question {
    min-width: 0;
    margin: 0;
    padding: 0;
    border: 0;
}

/* legend flutuante para quebrar linha e crescer como um título normal */
.question legend {
    float: left;
    width: 100%;
    max-width: 44rem;
    margin: 0 0 24px;
    padding: 0;
    font-size: clamp(1.3rem, 1rem + 1.2vw, 1.85rem);
    font-weight: 800;
    line-height: 1.25;
}

.options {
    clear: both;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 19rem), 1fr));
    gap: 16px;
}

/* alternativas em formato de tecla */
.option {
    position: relative;
    display: block;
    cursor: pointer;
}

/* o radio fica por cima, invisível, para continuar clicável e focável */
.option input {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    opacity: 0;
    cursor: pointer;
}

.option-body {
    display: flex;
    align-items: center;
    gap: 14px;
    height: 100%;
    min-height: 68px;
    padding: 12px 16px;
    border: 2px solid var(--line);
    border-radius: 18px;
    background: #fff;
    box-shadow: 0 5px 0 var(--line);
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.35;
    transition: transform 0.1s ease, box-shadow 0.1s ease, border-color 0.15s ease, background-color 0.15s ease;
}

.option:hover .option-body {
    border-color: #B5BAE8;
    box-shadow: 0 5px 0 #B5BAE8;
}

.option:active .option-body {
    transform: translateY(4px);
}

.option input:focus-visible + .option-body {
    outline: 3px solid var(--cobalt);
    outline-offset: 3px;
}

.option-key {
    flex: none;
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    border-radius: 11px;
    background: #E8EAFB;
    color: var(--cobalt);
    font-weight: 800;
    transition: background-color 0.15s ease, color 0.15s ease;
}

.option input:checked + .option-body {
    border-color: var(--cobalt);
    background: #EEF0FF;
    box-shadow: 0 5px 0 var(--cobalt);
}

.option input:checked + .option-body .option-key {
    background: var(--cobalt);
    color: #fff;
}

.option input:checked + .option-body.correct {
    border-color: var(--mint);
    background: var(--mint-soft);
    box-shadow: 0 5px 0 var(--mint);
}

.option input:checked + .option-body.correct .option-key {
    background: var(--mint);
    color: #fff;
}

.option input:checked + .option-body.wrong {
    border-color: var(--coral);
    background: var(--coral-soft);
    box-shadow: 0 5px 0 var(--coral);
    animation: tremer 0.4s ease;
}

.option input:checked + .option-body.wrong .option-key {
    background: var(--coral);
    color: #fff;
}

.actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 14px;
    margin-top: 26px;
}

/* resposta e explicação */
.feedback {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 16px 18px;
    margin-top: 24px;
    padding: 20px 22px;
    border-radius: 22px;
    animation: entra 0.28s ease-out;
}

.feedback.is-correct {
    background: var(--mint-soft);
}

.feedback.is-wrong {
    background: var(--coral-soft);
}

.feedback-icon {
    flex: none;
    display: grid;
    place-items: center;
    width: 46px;
    height: 46px;
    border-radius: 50%;
    color: #fff;
}

.is-correct .feedback-icon {
    background: var(--mint);
}

.is-wrong .feedback-icon {
    background: var(--coral);
}

.feedback-body {
    flex: 1 1 16rem;
    min-width: 0;
}

.feedback-title {
    margin: 0 0 4px;
    font-size: 1.2rem;
    font-weight: 800;
}

.is-correct .feedback-title {
    color: #0B5A3C;
}

.is-wrong .feedback-title {
    color: #8F1230;
}

.explanation {
    margin: 0;
    max-width: 60ch;
    color: var(--ink);
    font-size: 1rem;
}

.feedback .btn {
    margin-left: auto;
}

/* resultado */
.result {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
    width: 100%;
    max-width: 28rem;
    margin: auto;
    text-align: center;
}

.result-title {
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(1.4rem, 1.1rem + 1.2vw, 1.9rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

/* placar em balão de fala, o mesmo recurso do logotipo */
.score {
    position: relative;
    margin-bottom: 0.5rem;
    padding: 0.5rem 2.2rem 1rem;
    border-radius: 32px 32px 32px 8px;
    background: var(--sun);
    transform: rotate(-2deg);
}

.score::after {
    content: '';
    position: absolute;
    left: 28px;
    bottom: -16px;
    width: 26px;
    height: 18px;
    background: var(--sun);
    clip-path: polygon(0 0, 100% 0, 0 100%);
}

.score-value {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 8px;
    margin: 0;
    line-height: 1.1;
}

.score-number {
    font-family: var(--font-display);
    font-size: clamp(4rem, 3rem + 6vw, 6.5rem);
    font-weight: 800;
    letter-spacing: -0.04em;
}

.score-total {
    font-size: 1.5rem;
    font-weight: 800;
    opacity: 0.6;
}

.score-label {
    margin: 0;
    font-size: 1rem;
    font-weight: 700;
}

.save {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
}

@keyframes entra {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: none;
    }
}

@keyframes tremer {
    20% { transform: translateX(-6px); }
    40% { transform: translateX(5px); }
    60% { transform: translateX(-3px); }
    80% { transform: translateX(2px); }
}

@media (max-width: 36rem) {
    .feedback .btn {
        width: 100%;
        margin-left: 0;
    }

    .actions .btn {
        width: 100%;
    }
}

</style>