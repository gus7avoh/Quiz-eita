<script lang="ts" setup>
import { ref, watch } from 'vue'
import RankingBar from './RankingBar.vue'
import SelectGame from './SelectGame.vue';

const rankingAberto = ref(false)
const quizEmJogo = ref(false)

watch(quizEmJogo, (emJogo) => {
    if (emJogo) rankingAberto.value = false
})
</script>

<template>
    <section class="janela">

        <header class="topo">
            <h1 class="title">Eita Quiz</h1>
            <span class="sub_title">Encontro integrador de tecnologia Anhanguera</span>
        </header>

        <div class="content_wrapper">

            <aside
                id="ranking-mobile-panel"
                :class="{ 'ranking-open': rankingAberto }"
                :role="rankingAberto ? 'dialog' : undefined"
                :aria-modal="rankingAberto ? 'true' : undefined"
                :aria-labelledby="rankingAberto ? 'ranking-mobile-title' : undefined"
            >
                <div class="ranking-mobile-header">
                    <h2 id="ranking-mobile-title">Ranking</h2>
                    <button class="ranking-close" type="button" aria-label="Fechar ranking" @click="rankingAberto = false">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <RankingBar/>
            </aside>

            <main>
                <SelectGame @quiz-ativo="quizEmJogo = $event" />
            </main>

        </div>

        <nav v-if="!quizEmJogo" class="mobile-bottom-nav" aria-label="Menu da tela de criação">
            <button
                class="ranking-toggle"
                type="button"
                :aria-expanded="rankingAberto"
                aria-controls="ranking-mobile-panel"
                @click="rankingAberto = true"
            >
                <span class="ranking-toggle-icon" aria-hidden="true">★</span>
                <span>Ranking</span>
            </button>
        </nav>

    </section>
</template>

<!--
  ESTILOS GLOBAIS (tokens de design + peças compartilhadas).
  Os outros três componentes dependem das variáveis definidas aqui.
-->
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Unbounded:wght@600;800&display=swap');

:root {
    /* cores */
    --cobalt: #202a9ed7;
    --ink: #14123B;
    --paper: #F4F5FF;
    --sun: #FFC933;
    --sun-edge: #D9A100;
    --mint: #14A56F;
    --mint-soft: #DDF6EA;
    --coral: #F0405F;
    --coral-soft: #FFE3E8;
    --line: #D6D9F3;
    --muted: #5B5E8A;

    /* cor de cada dificuldade (usada em chips e no ranking) */
    --d-facil: #1FBF85;
    --d-medio: #FFB020;
    --d-dificil: #FF5A7A;
    --d-impossivel: #8F6BFF;

    /* forma e tipografia */
    --radius-lg: 28px;
    --font-display: 'Unbounded', 'Arial Black', system-ui, sans-serif;
    --font-body: 'Figtree', system-ui, -apple-system, 'Segoe UI', sans-serif;

    color-scheme: light;
}

*, *::before, *::after {
    box-sizing: border-box;
}

/* !important garante que a aplicação respeite a altura da janela mesmo
   com estilos globais antigos. */
html {
    height: 100% !important;
    overflow-x: hidden;
    overflow-y: hidden !important;
    background: var(--cobalt) !important;
}

html body {
    margin: 0;
    display: block !important;
    height: 100% !important;
    min-width: 320px;
    overflow: hidden !important;
    background: var(--cobalt) !important;
    color: var(--ink);
    font-family: var(--font-body);
    font-size: 16px;
    line-height: 1.5;
    text-align: left;
    -webkit-font-smoothing: antialiased;
}

html body #app {
    display: block !important;
    width: auto !important;
    height: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: transparent !important;
    text-align: left;
}

/* Em telas pequenas, o conteúdo do jogo define a altura da página e a
   rolagem fica no documento, em vez de ficar presa em um painel interno. */
@media (max-width: 48rem) {
    html,
    html body,
    html body #app {
        height: auto !important;
        min-height: 100%;
        overflow-x: hidden !important;
        overflow-y: auto !important;
    }
}

* {
    scrollbar-width: thin;
    scrollbar-color: var(--cobalt) transparent;
}

*::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

*::-webkit-scrollbar-track {
    background: transparent;
}

*::-webkit-scrollbar-thumb {
    border: 3px solid transparent;
    border-radius: 999px;
    background: var(--cobalt);
    background-clip: padding-box;
}

*::-webkit-scrollbar-thumb:hover {
    background: var(--ink);
    background-clip: padding-box;
}

/* botão principal: tecla com "borda" inferior que afunda ao clicar */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    min-height: 56px;
    padding: 0 30px;
    border: 0;
    border-radius: 16px;
    background: var(--sun);
    color: var(--ink);
    font-family: var(--font-body);
    font-size: 1.05rem;
    font-weight: 800;
    line-height: 1;
    cursor: pointer;
    box-shadow: 0 5px 0 var(--sun-edge);
    transition: transform 0.1s ease, box-shadow 0.1s ease, background-color 0.15s ease;
}

.btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 0 var(--sun-edge);
}

.btn:active:not(:disabled) {
    transform: translateY(4px);
    box-shadow: 0 1px 0 var(--sun-edge);
}

.btn:focus-visible {
    outline: 3px solid var(--cobalt);
    outline-offset: 3px;
}

.btn:disabled {
    background: #E1E3F6;
    color: #7F82A9;
    box-shadow: 0 5px 0 #C9CCEA;
    cursor: not-allowed;
}

/* campo de texto */
.text-input {
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
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.text-input::placeholder {
    color: #6F7299;
    font-weight: 500;
}

.text-input:focus {
    outline: none;
    border-color: var(--cobalt);
    box-shadow: 0 0 0 4px rgba(47, 63, 224, 0.2);
}

/* mensagem de erro */
.error-msg {
    margin: 0;
    padding: 12px 16px;
    border-radius: 14px;
    background: var(--coral-soft);
    color: #8F1230;
    font-size: 0.95rem;
    font-weight: 700;
}

/* bolinha de cor da dificuldade */
.dot {
    flex: none;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--dot, #999);
}
.dot-facil { --dot: var(--d-facil); }
.dot-medio { --dot: var(--d-medio); }
.dot-dificil { --dot: var(--d-dificil); }
.dot-impossivel { --dot: var(--d-impossivel); }
.dot-misto {
    background: conic-gradient(var(--d-facil), var(--d-medio), var(--d-dificil), var(--d-impossivel), var(--d-facil));
}

/* texto só para leitores de tela */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>

<style scoped>
.janela {
    display: flex;
    flex-direction: column;
    gap: clamp(16px, 2.2vw, 28px);
    padding: clamp(16px, 2.5vw, 32px);
    overflow: hidden;
    border-radius: var(--radius-lg);
}

.topo {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: clamp(16px, 2vw, 28px);
    padding-bottom: 0.3rem;
}

/* logotipo em balão de fala */
.title {
    position: relative;
    margin: 0;
    padding: 0.35em 0.6em 0.4em;
    border-radius: 0.55em 0.55em 0.55em 0.12em;
    background: var(--sun);
    color: var(--ink);
    font-family: var(--font-display);
    font-size: clamp(1.75rem, 1.1rem + 2.2vw, 2.9rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1;
    transform: rotate(-2deg);
    animation: balao-entra 0.5s cubic-bezier(0.2, 1.4, 0.4, 1) both;
}

.title::after {
    content: '';
    position: absolute;
    left: 0.45em;
    bottom: -0.28em;
    width: 0.5em;
    height: 0.34em;
    background: var(--sun);
    clip-path: polygon(0 0, 100% 0, 0 100%);
}

.sub_title {
    display: block;
    max-width: 24ch;
    color: rgba(255, 255, 255, 0.92);
    font-size: clamp(0.95rem, 0.85rem + 0.4vw, 1.15rem);
    font-weight: 600;
    line-height: 1.3;
}

.content_wrapper {
    flex: 1;
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(17rem, 22rem);
    gap: clamp(16px, 2vw, 28px);
    min-height: 0;
    overflow: hidden;
}

/* o jogo fica na coluna principal; o ranking, ao lado */
.content_wrapper main {
    grid-column: 1;
    grid-row: 1;
    display: flex;
    min-width: 0;
    min-height: 0;
}

.content_wrapper main :deep(#janela) {
    min-height: 0;
    overflow-y: auto;
}

.content_wrapper aside {
    grid-column: 2;
    grid-row: 1;
    position: relative;
    min-width: 0;
    min-height: 0;
}

/* o ranking rola por dentro e nunca estica a página */
.content_wrapper aside :deep(.side-bar) {
    position: absolute;
    inset: 0;
}

@media (max-width: 62rem) {
    .content_wrapper {
        grid-template-columns: minmax(0, 1fr);
        grid-template-rows: minmax(20rem, 1fr) minmax(12rem, 0.65fr);
        overflow-y: auto;
    }

    .content_wrapper aside {
        grid-column: 1;
        grid-row: 2;
        height: auto;
        min-height: 0;
    }
}

.mobile-bottom-nav {
    display: none;
}

.ranking-mobile-header {
    display: none;
}

@media (max-width: 48rem) {
    .janela {
        padding-bottom: calc(76px + env(safe-area-inset-bottom));
        overflow: visible;
    }

    .content_wrapper {
        display: block;
        flex: none;
        overflow: visible;
    }

    .content_wrapper aside {
        display: none;
    }

    .content_wrapper aside.ranking-open {
        position: fixed;
        inset: 0;
        /* O ranking aberto ocupa a tela e precisa ficar acima do botão de
           configurações, que permanece disponível no restante do fluxo. */
        z-index: 50;
        display: flex;
        flex-direction: column;
        padding: max(16px, env(safe-area-inset-top)) 16px max(16px, env(safe-area-inset-bottom));
        background: var(--ink);
        color: #fff;
    }

    .content_wrapper aside.ranking-open :deep(.side-bar) {
        position: relative;
        inset: auto;
        flex: 1;
        height: auto;
        padding: 8px 0 0;
        border-radius: 0;
    }

    .content_wrapper main {
        grid-column: 1;
        grid-row: 1;
        display: block;
        min-height: auto;
    }

    .content_wrapper main :deep(#janela) {
        min-height: auto;
        overflow: visible;
    }

    .mobile-bottom-nav {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 20;
        display: flex;
        justify-content: center;
        padding: 10px 16px calc(10px + env(safe-area-inset-bottom));
        background: rgba(20, 18, 59, 0.96);
        box-shadow: 0 -8px 24px rgba(20, 18, 59, 0.18);
    }

    .ranking-toggle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: min(100%, 22rem);
        min-height: 48px;
        border: 0;
        border-radius: 999px;
        background: var(--sun);
        color: var(--ink);
        font: 800 1rem/1 var(--font-body);
        cursor: pointer;
    }

    .ranking-toggle:focus-visible,
    .ranking-close:focus-visible {
        outline: 3px solid var(--sun);
        outline-offset: 3px;
    }

    .ranking-toggle-icon {
        font-size: 1.15rem;
    }

    .ranking-mobile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 12px;
    }

    .ranking-mobile-header h2 {
        margin: 0;
        font-family: var(--font-display);
        font-size: 1.35rem;
        line-height: 1.1;
    }

    .ranking-close {
        display: grid;
        place-items: center;
        width: 44px;
        height: 44px;
        border: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.12);
        color: #fff;
        font: 400 2rem/1 var(--font-body);
        cursor: pointer;
    }

    .content_wrapper aside.ranking-open :deep(.title h1) {
        display: none;
    }

    .content_wrapper aside.ranking-open :deep(.ranking-list) {
        padding-right: 0;
    }
}

@keyframes balao-entra {
    from {
        opacity: 0;
        transform: rotate(-8deg) scale(0.85);
    }
    to {
        opacity: 1;
        transform: rotate(-2deg) scale(1);
    }
}
</style>
