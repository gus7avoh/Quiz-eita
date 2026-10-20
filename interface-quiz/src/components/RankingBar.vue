<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'
import type { Ranking, Usuario } from '../types/QuizTypes';
import { mockadoBuscarusuarios } from '../service/QuizService';

const lista_ranking = ref<Ranking>({
    'facil': [],
    'medio': [],
    'dificil': [],
    'impossivel': [],
    'misto': []
})

const lista_atual = ref<Usuario[] | null> ([{'nome': 'davi', 'pontos': 20}])
let timer: ReturnType<typeof setInterval> | undefined


async function carregarRanking() {

    try{
        lista_ranking.value = await mockadoBuscarusuarios()

    } catch (error) {
        console.error('Erro ao buscar ranking:', error)
    }
}

onMounted(() => {

    carregarRanking()
    timer = setInterval(async () => {
        
        await adicionarUsuariosAleatorios()
        await organizarLista()
    }, 10_000)
    
})

onUnmounted(() => {clearInterval(timer)})

function mudarLista(ranking_dificuldade: string) {
    switch(ranking_dificuldade) {

        case 'facil':
            lista_atual.value=lista_ranking.value.facil
            break

        case 'medio':
            lista_atual.value=lista_ranking.value.medio
            break

        case 'dificil':
            lista_atual.value=lista_ranking.value.dificil
            break

        case 'impossivel':
            lista_atual.value=lista_ranking.value.impossivel
            break

        case 'misto':
            lista_atual.value=lista_ranking.value.misto
            break
    }
}
async function adicionarUsuariosAleatorios() {
    lista_ranking.value.facil.push({nome: 'kratos', pontos: Math.floor(Math.random() * 100)})
        lista_ranking.value.medio.push({nome: 'Allay', pontos: Math.floor(Math.random() * 100)})
        lista_ranking.value.dificil.push({nome: 'Steve', pontos: Math.floor(Math.random() * 100)})
        lista_ranking.value.impossivel.push({nome: 'madagascar', pontos: Math.floor(Math.random() * 100)})
        lista_ranking.value.misto.push({nome: 'Minto', pontos: Math.floor(Math.random() * 100)})
}
async function organizarLista() {
    lista_ranking.value.facil.sort((a, b) => b.pontos - a.pontos)
    lista_ranking.value.medio.sort((a, b) => b.pontos - a.pontos)
    lista_ranking.value.dificil.sort((a, b) => b.pontos - a.pontos)
    lista_ranking.value.impossivel.sort((a, b) => b.pontos - a.pontos)
    lista_ranking.value.misto.sort((a, b) => b.pontos - a.pontos)
}

</script>

<template>
    
    <section class="side-bar">

        <div class="title">

            <h1>Ranking</h1>

            <div class="radio-input" role="radiogroup" aria-label="Dificuldade do ranking">

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('facil')"/>
                    <span class="check"><span class="dot dot-facil"></span>Fácil</span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio"  @click="mudarLista('medio')"/>
                    <span class="check"><span class="dot dot-medio"></span>Médio</span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('dificil')"/>
                    <span class="check"><span class="dot dot-dificil"></span>Difícil</span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('impossivel')"/>
                    <span class="check"><span class="dot dot-impossivel"></span>Impossível</span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('misto')"/>
                    <span class="check"><span class="dot dot-misto"></span>Misto</span>
                </label>

            </div>

        </div>

        <div class="ranking-list">

            <p v-if="!lista_atual || !lista_atual.length" class="empty">
                Ainda não há jogadores nesta dificuldade.
            </p>

            <div v-for="(Usuario, index) in lista_atual"
            class="ranking-item"
            :class="index < 3 ? 'podium podium-' + (index + 1) : ''"
            >
                <span class="pos">{{ index + 1 }}</span>
                <span class="name">{{ Usuario.nome }}</span>
                <span class="points">{{ Usuario.pontos }}<small>pts</small></span>
            </div>

        </div>

    </section>
</template>

<style scoped>

.side-bar {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    min-width: 0;
    min-height: 0;
    padding: clamp(18px, 2vw, 26px);
    background: var(--ink);
    color: #fff;
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.title {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin: 0 0 18px;
}

.title h1 {
    margin: 0;
    color: #fff;
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

/* abas de dificuldade */
.radio-input {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.radio-input .label {
    position: relative;
    display: flex;
}

/* o radio fica por cima, invisível, para continuar clicável e focável */
.radio-input .label input {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    opacity: 0;
    cursor: pointer;
}

.radio-input .label .check {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    height: 36px;
    padding: 0 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.84);
    font-size: 0.9rem;
    font-weight: 700;
    transition: background-color 0.15s ease, color 0.15s ease;
}

.radio-input .label:hover .check {
    background: rgba(255, 255, 255, 0.16);
}

.radio-input .label input:checked + .check {
    background: #fff;
    color: var(--ink);
}

.radio-input .label input:focus-visible + .check {
    outline: 3px solid var(--sun);
    outline-offset: 2px;
}

/* lista */
.ranking-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 0;
    padding-right: 4px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.ranking-item {
    display: grid;
    grid-template-columns: 2rem minmax(0, 1fr) auto;
    align-items: center;
    gap: 12px;
    padding: 10px 14px 10px 10px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.07);
    font-size: 1rem;
}

.pos {
    display: grid;
    place-items: center;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    color: rgba(255, 255, 255, 0.72);
    font-size: 0.9rem;
    font-weight: 800;
}

.podium-1 {
    background: rgba(255, 201, 51, 0.18);
}

.podium-1 .pos {
    background: #FFC933;
    color: var(--ink);
}

.podium-2 .pos {
    background: #CBD0EA;
    color: var(--ink);
}

.podium-3 .pos {
    background: #e7602b;
    color: var(--ink);
}

.name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-weight: 700;
}

.points {
    font-weight: 800;
    font-variant-numeric: tabular-nums;
}

.points small {
    margin-left: 4px;
    color: rgba(255, 255, 255, 0.65);
    font-size: 0.75rem;
    font-weight: 600;
}

.empty {
    margin: 0;
    padding: 14px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.07);
    color: rgba(255, 255, 255, 0.78);
    font-size: 0.95rem;
}

</style>