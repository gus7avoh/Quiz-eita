<script lang="ts" setup>
import { ref } from 'vue'

const props = defineProps<{
  musicaAtiva: boolean
  vozAtiva: boolean
  falaAtiva: boolean
  volumeMusica: number
}>()

const emit = defineEmits<{
  (event: 'alternar-musica'): void
  (event: 'alternar-voz'): void
  (event: 'alternar-fala'): void
  (event: 'volume-change', volume: number): void
}>()

const aberto = ref(false)

function alterarVolume(event: Event) {
  const input = event.target as HTMLInputElement
  emit('volume-change', Number(input.value) / 100)
}
</script>

<template>
  <section class="settings" aria-label="Configurações do jogo">
    <button
      class="setting-btn"
      type="button"
      :aria-expanded="aberto"
      aria-controls="game-settings-panel"
      :aria-label="aberto ? 'Fechar configurações' : 'Abrir configurações'"
      @click="aberto = !aberto"
    >
      <span class="bar bar1" aria-hidden="true"></span>
      <span class="bar bar2" aria-hidden="true"></span>
      <span class="bar bar1" aria-hidden="true"></span>
    </button>

    <div
      v-if="aberto"
      id="game-settings-panel"
      class="settings-panel"
      role="dialog"
      aria-modal="false"
      aria-labelledby="game-settings-title"
    >
      <div class="settings-heading">
        <div>
          <h2 id="game-settings-title">Configurações</h2>
          <p>Ative somente os recursos que quiser usar.</p>
        </div>
        <button
          class="settings-close"
          type="button"
          aria-label="Fechar configurações"
          @click="aberto = false"
        >
          <span aria-hidden="true">×</span>
        </button>
      </div>

      <div class="settings-options">
        <div class="settings-option" :class="{ active: props.musicaAtiva }">
          <span class="option-copy">
            <strong>Música</strong>
            <small>Trilha sonora da partida</small>
          </span>
          <div class="cyber-toggle-wrapper">
            <input
              id="game-music-toggle"
              class="cyber-toggle-checkbox"
              type="checkbox"
              :checked="props.musicaAtiva"
              aria-label="Ativar música"
              @change="emit('alternar-musica')"
            />
            <label class="cyber-toggle" for="game-music-toggle">
              <span class="cyber-toggle-track">
                <span class="cyber-toggle-track-glow"></span>
                <span class="cyber-toggle-track-dots">
                  <span class="cyber-toggle-track-dot"></span>
                  <span class="cyber-toggle-track-dot"></span>
                  <span class="cyber-toggle-track-dot"></span>
                </span>
              </span>
              <span class="cyber-toggle-thumb">
                <span class="cyber-toggle-thumb-shadow"></span>
                <span class="cyber-toggle-thumb-highlight"></span>
                <span class="cyber-toggle-thumb-icon" aria-hidden="true">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M16.5 12c0-2.48-2.02-4.5-4.5-4.5s-4.5 2.02-4.5 4.5 2.02 4.5 4.5 4.5 4.5-2.02 4.5-4.5zm-4.5 7.5c-4.14 0-7.5-3.36-7.5-7.5s3.36-7.5 7.5-7.5 7.5 3.36 7.5 7.5-3.36 7.5-7.5 7.5zm0-16.5c-4.97 0-9 4.03-9 9h-3l3.89 3.89.07.14 4.04-4.03h-3c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42c1.63 1.63 3.87 2.64 6.36 2.64 4.97 0 9-4.03 9-9s-4.03-9-9-9z"></path>
                  </svg>
                </span>
              </span>
              <span class="cyber-toggle-particles" aria-hidden="true">
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
              </span>
            </label>
            <span class="cyber-toggle-labels" aria-hidden="true">
              <span class="cyber-toggle-label-off">OFF</span>
              <span class="cyber-toggle-label-on">ON</span>
            </span>
          </div>
        </div>

        <label class="volume-control" for="game-music-volume">
          <span>
            <strong>Volume</strong>
            <output for="game-music-volume">{{ Math.round(props.volumeMusica * 100) }}%</output>
          </span>
          <input
            id="game-music-volume"
            type="range"
            min="0"
            max="100"
            step="1"
            :value="Math.round(props.volumeMusica * 100)"
            aria-label="Volume da música"
            @input="alterarVolume"
          />
        </label>

        <div class="settings-option" :class="{ active: props.vozAtiva }">
          <span class="option-copy">
            <strong>Leitura em voz alta</strong>
            <small>Mostra o botão para ouvir a pergunta</small>
          </span>
          <div class="cyber-toggle-wrapper">
            <input
              id="game-voice-toggle"
              class="cyber-toggle-checkbox"
              type="checkbox"
              :checked="props.vozAtiva"
              aria-label="Ativar leitura em voz alta"
              @change="emit('alternar-voz')"
            />
            <label class="cyber-toggle" for="game-voice-toggle">
              <span class="cyber-toggle-track">
                <span class="cyber-toggle-track-glow"></span>
                <span class="cyber-toggle-track-dots">
                  <span class="cyber-toggle-track-dot"></span>
                  <span class="cyber-toggle-track-dot"></span>
                  <span class="cyber-toggle-track-dot"></span>
                </span>
              </span>
              <span class="cyber-toggle-thumb">
                <span class="cyber-toggle-thumb-shadow"></span>
                <span class="cyber-toggle-thumb-highlight"></span>
                <span class="cyber-toggle-thumb-icon" aria-hidden="true">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M16.5 12c0-2.48-2.02-4.5-4.5-4.5s-4.5 2.02-4.5 4.5 2.02 4.5 4.5 4.5 4.5-2.02 4.5-4.5zm-4.5 7.5c-4.14 0-7.5-3.36-7.5-7.5s3.36-7.5 7.5-7.5 7.5 3.36 7.5 7.5-3.36 7.5-7.5 7.5zm0-16.5c-4.97 0-9 4.03-9 9h-3l3.89 3.89.07.14 4.04-4.03h-3c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42c1.63 1.63 3.87 2.64 6.36 2.64 4.97 0 9-4.03 9-9s-4.03-9-9-9z"></path>
                  </svg>
                </span>
              </span>
              <span class="cyber-toggle-particles" aria-hidden="true">
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
              </span>
            </label>
            <span class="cyber-toggle-labels" aria-hidden="true">
              <span class="cyber-toggle-label-off">OFF</span>
              <span class="cyber-toggle-label-on">ON</span>
            </span>
          </div>
        </div>

        <div class="settings-option" :class="{ active: props.falaAtiva }">
          <span class="option-copy">
            <strong>Resposta por voz</strong>
            <small>Mostra o botão para responder falando</small>
          </span>
          <div class="cyber-toggle-wrapper">
            <input
              id="game-speech-toggle"
              class="cyber-toggle-checkbox"
              type="checkbox"
              :checked="props.falaAtiva"
              aria-label="Ativar resposta por voz"
              @change="emit('alternar-fala')"
            />
            <label class="cyber-toggle" for="game-speech-toggle">
              <span class="cyber-toggle-track">
                <span class="cyber-toggle-track-glow"></span>
                <span class="cyber-toggle-track-dots">
                  <span class="cyber-toggle-track-dot"></span>
                  <span class="cyber-toggle-track-dot"></span>
                  <span class="cyber-toggle-track-dot"></span>
                </span>
              </span>
              <span class="cyber-toggle-thumb">
                <span class="cyber-toggle-thumb-shadow"></span>
                <span class="cyber-toggle-thumb-highlight"></span>
                <span class="cyber-toggle-thumb-icon" aria-hidden="true">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M16.5 12c0-2.48-2.02-4.5-4.5-4.5s-4.5 2.02-4.5 4.5 2.02 4.5 4.5 4.5 4.5-2.02 4.5-4.5zm-4.5 7.5c-4.14 0-7.5-3.36-7.5-7.5s3.36-7.5 7.5-7.5 7.5 3.36 7.5 7.5-3.36 7.5-7.5 7.5zm0-16.5c-4.97 0-9 4.03-9 9h-3l3.89 3.89.07.14 4.04-4.03h-3c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42c1.63 1.63 3.87 2.64 6.36 2.64 4.97 0 9-4.03 9-9s-4.03-9-9-9z"></path>
                  </svg>
                </span>
              </span>
              <span class="cyber-toggle-particles" aria-hidden="true">
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
                <span class="cyber-toggle-particle"></span>
              </span>
            </label>
            <span class="cyber-toggle-labels" aria-hidden="true">
              <span class="cyber-toggle-label-off">OFF</span>
              <span class="cyber-toggle-label-on">ON</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.settings {
  position: fixed;
  top: max(14px, env(safe-area-inset-top));
  right: max(14px, env(safe-area-inset-right));
  z-index: 40;
  color: var(--ink);
}

.settings-close {
  display: grid;
  place-items: center;
  border: 0;
  cursor: pointer;
}

.setting-btn {
  width: 45px;
  height: 45px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0;
  border: none;
  border-radius: 10px;
  background-color: rgb(129, 110, 216);
  box-shadow: 0 0 0 2px rgb(212, 209, 255);
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.setting-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 0 2px rgb(212, 209, 255), 0 6px 14px rgba(20, 18, 59, 0.22);
}

.setting-btn:active {
  transform: translateY(2px);
}

.bar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50%;
  height: 2px;
  border-radius: 2px;
  background-color: rgb(229, 229, 229);
}

.bar::before {
  content: '';
  position: absolute;
  width: 2px;
  height: 2px;
  border: 2px solid #fff;
  border-radius: 50%;
  background-color: rgb(126, 117, 255);
  box-shadow: 0 0 5px #fff;
  transition: all 0.3s;
}

.bar1::before {
  transform: translateX(-4px);
}

.bar2::before {
  transform: translateX(4px);
}

.setting-btn:hover .bar1::before {
  transform: translateX(4px);
}

.setting-btn:hover .bar2::before {
  transform: translateX(-4px);
}

.setting-btn:focus-visible,
.settings-close:focus-visible,
.volume-control input:focus-visible,
.cyber-toggle-checkbox:focus-visible + .cyber-toggle {
  outline: 3px solid var(--sun);
  outline-offset: 3px;
}

.settings-panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: min(22rem, calc(100vw - 28px));
  margin-top: 0;
  padding: 18px;
  border: 2px solid rgba(20, 18, 59, 0.08);
  border-radius: 22px;
  background: #fff;
  box-shadow: 0 16px 38px rgba(20, 18, 59, 0.25);
}

.settings-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.settings-heading h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.05rem;
  line-height: 1.2;
}

.settings-heading p {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 0.85rem;
  line-height: 1.3;
}

.settings-close {
  flex: none;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #eef0ff;
  color: var(--ink);
  font-size: 1.45rem;
  line-height: 1;
}

.settings-options {
  display: grid;
  gap: 10px;
}

.settings-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  width: 100%;
  min-height: 58px;
  padding: 10px 12px;
  border: 2px solid var(--line);
  border-radius: 15px;
  background: #fff;
  color: var(--ink);
  text-align: left;
  transition: border-color 0.15s ease, background-color 0.15s ease;
}

.settings-option:hover {
  border-color: #aeb5e5;
}

.settings-option.active {
  border-color: var(--mint);
  background: var(--mint-soft);
}

.option-copy {
  display: grid;
  gap: 2px;
  min-width: 0;
}

.option-copy strong {
  font-size: 0.95rem;
}

.option-copy small {
  color: var(--muted);
  font-size: 0.77rem;
  line-height: 1.25;
}

.volume-control {
  display: grid;
  gap: 8px;
  padding: 4px 4px 8px;
  color: var(--ink);
  cursor: pointer;
}

.volume-control > span {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 0.9rem;
}

.volume-control output {
  color: var(--muted);
  font-weight: 800;
}

.volume-control input {
  width: 100%;
  accent-color: var(--cobalt);
  cursor: pointer;
}

/* Switch Cyber Toggle adaptado do exemplo do Uiverse. */
.cyber-toggle-wrapper {
  display: inline-flex;
  flex: none;
  flex-direction: column;
  align-items: center;
  position: relative;
  padding: 4px 0 0;
}

.cyber-toggle-checkbox {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.cyber-toggle {
  position: relative;
  display: inline-block;
  width: 64px;
  height: 32px;
  cursor: pointer;
}

.cyber-toggle-track {
  position: absolute;
  inset: 0;
  overflow: hidden;
  border-radius: 16px;
  background: #111;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5), inset 0 0 4px rgba(0, 0, 0, 0.8);
  transition: all 0.4s cubic-bezier(0.3, 1.5, 0.7, 1);
}

.cyber-toggle-track::before {
  content: '';
  position: absolute;
  inset: 2px;
  z-index: 0;
  border-radius: 14px;
  background: #222;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);
  transition: all 0.4s ease;
}

.cyber-toggle-track-glow {
  position: absolute;
  inset: 0;
  z-index: 1;
  border-radius: 16px;
  background: linear-gradient(90deg, #03e9f4, #4a00e0);
  opacity: 0;
  transition: all 0.4s ease;
}

.cyber-toggle-thumb {
  position: absolute;
  top: 4px;
  left: 4px;
  z-index: 2;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #151515;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4);
  transition: all 0.4s cubic-bezier(0.3, 1.5, 0.7, 1);
}

.cyber-toggle-thumb-shadow,
.cyber-toggle-thumb-highlight {
  position: absolute;
  inset: 0;
  z-index: 1;
  border-radius: 50%;
}

.cyber-toggle-thumb-shadow {
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.1), transparent 70%);
}

.cyber-toggle-thumb-highlight {
  background: radial-gradient(circle at 70% 70%, rgba(0, 0, 0, 0.2), transparent 70%);
}

.cyber-toggle-thumb-icon {
  position: absolute;
  inset: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.cyber-toggle-thumb-icon svg {
  width: 14px;
  height: 14px;
  fill: #555;
  transition: fill 0.4s ease, transform 0.4s ease;
}

.cyber-toggle-track-dots {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 10px;
}

.cyber-toggle-track-dot {
  width: 3px;
  height: 3px;
  margin-left: 3px;
  border-radius: 50%;
  background: #444;
  opacity: 0.5;
  transition: all 0.4s ease;
}

.cyber-toggle-particles {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.cyber-toggle-particle {
  position: absolute;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: #03e9f4;
  opacity: 0;
  filter: blur(1px);
  box-shadow: 0 0 4px rgba(3, 233, 244, 0.8);
  transition: all 0.3s ease;
}

.cyber-toggle-particle:nth-child(1) { top: 15%; right: 20%; }
.cyber-toggle-particle:nth-child(2) { top: 45%; right: 30%; }
.cyber-toggle-particle:nth-child(3) { top: 25%; right: 40%; }
.cyber-toggle-particle:nth-child(4) { top: 60%; right: 15%; }

.cyber-toggle-labels {
  display: flex;
  justify-content: space-between;
  width: 64px;
  margin-top: 5px;
  color: #555;
  font: 600 9px/1 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  letter-spacing: 0.7px;
  text-transform: uppercase;
}

.cyber-toggle-label-off,
.cyber-toggle-label-on {
  transition: all 0.4s ease;
}

.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-track-glow {
  opacity: 0.5;
}

.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-thumb {
  left: calc(100% - 28px);
  background: #222;
}

.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-thumb-icon {
  transform: rotate(360deg);
}

.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-thumb-icon svg {
  fill: #03e9f4;
}

.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-track-dot {
  background: #03e9f4;
  box-shadow: 0 0 4px #03e9f4;
  opacity: 1;
}

.cyber-toggle-checkbox:checked ~ .cyber-toggle-labels .cyber-toggle-label-on {
  color: #03e9f4;
  text-shadow: 0 0 5px rgba(3, 233, 244, 0.5);
}

.cyber-toggle-checkbox:not(:checked) ~ .cyber-toggle-labels .cyber-toggle-label-off {
  color: #aaa;
}

.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-particle {
  opacity: 1;
  animation: cyber-toggle-float 3s infinite alternate;
}

.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-particle:nth-child(1) { animation-delay: 0s; }
.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-particle:nth-child(2) { animation-delay: 0.5s; }
.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-particle:nth-child(3) { animation-delay: 1s; }
.cyber-toggle-checkbox:checked + .cyber-toggle .cyber-toggle-particle:nth-child(4) { animation-delay: 1.5s; }

.cyber-toggle:hover .cyber-toggle-track::before {
  background: #272727;
}

.cyber-toggle:hover .cyber-toggle-thumb {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
}

.cyber-toggle-checkbox:checked + .cyber-toggle:hover .cyber-toggle-track-glow {
  opacity: 0.7;
}

@keyframes cyber-toggle-float {
  0% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
  100% { transform: translateY(0); }
}

@media (max-width: 30rem) {
  .settings {
    top: max(10px, env(safe-area-inset-top));
    right: max(10px, env(safe-area-inset-right));
  }

  .settings-panel {
    max-height: calc(100dvh - 76px);
    overflow-y: auto;
  }
}
</style>
