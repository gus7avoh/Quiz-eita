<script lang="ts" setup>
import RankingBar from './RankingBar.vue'
import SelectGame from './SelectGame.vue';
</script>

<template>
    <section class="janela">

        <header class="topo">
            <h1 class="title">Eita Quiz</h1>
            <span class="sub_title">Encontro integrador de tecnologia Anhanguera</span>
        </header>

        <div class="content_wrapper">

            <aside>
                <RankingBar/>
            </aside>

            <main>
                <SelectGame/>
            </main>

        </div>

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

/* !important aqui é de propósito: garante que a página role e que o fundo
   seja o do tema, mesmo que exista um CSS global antigo travando
   altura/overflow ou pintando o fundo de escuro. */
html {
    height: auto !important;
    overflow-x: hidden;
    overflow-y: auto !important;
    background: var(--cobalt) !important;
}

html body {
    margin: 0;
    display: block !important;
    height: auto !important;
    min-width: 320px;
    min-height: 100dvh;
    overflow: visible !important;
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
    height: auto !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
    background: transparent !important;
    text-align: left;
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
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    gap: clamp(16px, 2.2vw, 28px);
    padding: clamp(16px, 2.5vw, 32px);
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
    font-size: clamp(1.9rem, 1.2rem + 2.6vw, 3.2rem);
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
}

/* o jogo fica na coluna principal; o ranking, ao lado */
.content_wrapper main {
    grid-column: 1;
    grid-row: 1;
    display: flex;
    min-width: 0;
    min-height: 0;
}

.content_wrapper aside {
    grid-column: 2;
    grid-row: 1;
    position: relative;
    min-width: 0;
    min-height: 30rem;
}

/* o ranking rola por dentro e nunca estica a página */
.content_wrapper aside :deep(.side-bar) {
    position: absolute;
    inset: 0;
}

@media (max-width: 62rem) {
    .content_wrapper {
        grid-template-columns: minmax(0, 1fr);
    }

    .content_wrapper aside {
        grid-column: 1;
        grid-row: 2;
        height: 28rem;
        min-height: 0;
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