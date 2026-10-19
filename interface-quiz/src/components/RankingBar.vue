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

            <div class="radio-input">

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('facil')"/>
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio"  @click="mudarLista('medio')"/>
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('dificil')"/>
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('impossivel')"/>
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" @click="mudarLista('misto')"/>
                    <span class="check"></span>
                </label>

            </div>
            
            <h1>Ranking</h1>

        </div>

        <!-- <div v-for="(player, index) in ranking"
            :key="player"
            class="ranking-item"
            :class="index % 2 === 0 ? 'light' : 'dark'"
        >
            {{ player }}
        </div> -->

        <div v-for="(Usuario, index) in lista_atual"
        class="ranking-item"
        :class="index % 2 === 0 ? 'light' : 'dark'"
        >
            {{ Usuario.nome }} {{ Usuario.pontos }}
        </div> 

    </section>
</template>

<style scoped>

.side-bar {
    box-sizing: border-box;
    padding: 20px;
    min-height: 0;
    min-width: 0;
    width:100%;
    height: 100%;
    background-color: #444;
    border-radius: 15px;
    overflow: hidden;
    
}

.title {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 1.01rem;
    font-family: 'Rubik Marker Hatch', cursive;
    font-weight: normal;
    color: var(--primary-color);
    margin: 0 0 20px 0;
}

.title h1 {
    margin: 10px 0 0 0;
}

.radio-input {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: clamp(8px, 2vw, 20px);
}

.radio-input .label input {
    display: none;
}

.radio-input .label {
    display: flex;
}

.radio-input .label .check {
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    cursor: pointer;
    transition: 0.3s;
    border: 3px solid transparent;
    box-shadow:
        3px 3px 6px rgba(0, 0, 0, 0.5),
        -1px -1px 4px rgba(255, 255, 255, 0.5);
}

.radio-input .label input:checked + .check {
    box-shadow:
        3px 3px 6px rgba(0, 0, 0, 0.5),
        -1px -1px 4px rgba(255, 255, 255, 0.5),
        inset 3px 3px 6px rgba(0, 0, 0, 0.5),
        inset -1px -1px 4px rgba(255, 255, 255, 0.5);

    transform: scale(1.1);
}

.ranking-item {
    padding: 10px;
    border-radius: 5px;
    color: #fff;
    font-size: 1rem;
    font-family: 'Courier New', monospace;
    margin-bottom: 10px;
    font-weight: bold;
}

.light {
    background-color: #555;
}

.dark {
    background-color: #3a3a3a;
}

</style>