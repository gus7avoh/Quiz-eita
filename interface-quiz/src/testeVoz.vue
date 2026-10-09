<script setup lang="ts">
import { ref } from "vue";
import { ouvindoUsuario, falar } from "./speechRecognitionService"

const textoOuvido = ref("");
const erro = ref("");

async function testarFalar() {
  erro.value = "";
  try {
    await falar(" Cynthia queremos 2000 pontos em prova pelo trabalho. Teste de voz funcionando com sucesso!");
  } catch (e) {
    erro.value = (e as Error).message;
  }
}

async function testarOuvir() {
  erro.value = "";
  try {
    textoOuvido.value = await ouvindoUsuario();
  } catch (e) {
    erro.value = (e as Error).message;
  }
}
</script>

<template>
  <div>
    <button @click="testarFalar">Testar fala</button>
    <button @click="testarOuvir">Testar escuta</button>
    <p>Ouvi: {{ textoOuvido }}</p>
    <p v-if="erro">Erro: {{ erro }}</p>
  </div>
</template>