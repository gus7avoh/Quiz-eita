<script setup lang="ts">
import { ref } from "vue";
import { ouvindoUsuario, falar } from "./service/speechRecognitionService";

const erro = ref("");
const status = ref("");
const respostas = ref<{ enunciado: string; resposta: string }[]>([]);

const LETRAS = ["a", "b", "c", "d"];
const SINONIMOS: Record<string, string[]> = {
  a: ["a"], b: ["b", "be"], c: ["c", "ce", "se"], d: ["d", "de"],
};

const perguntas = [
  { enunciado: "Qual a capital do Brasil?", alternativas: ["São Paulo", "Brasília", "Rio de Janeiro", "Salvador"] },
  { enunciado: "Quanto é 2 mais 2?", alternativas: ["3", "4", "5", "22"] },
];

function normalizar(s: string) {
  return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[.,!?]/g, "").trim();
}

function interpretar(fala: string, alternativas: string[]): string | null {
  const f = normalizar(fala);
  if (!f) return null;

  const porTexto = alternativas.find((a) => {
    const n = normalizar(a);
    return f.includes(n) || n.includes(f);
  });
  if (porTexto) return porTexto;

  const palavras = f.split(/\s+/);
  for (let i = 0; i < alternativas.length; i++) {
    if (SINONIMOS[LETRAS[i]].some((s) => palavras.includes(s))) return alternativas[i];
  }
  return null;
}

async function testarQuiz() {
  erro.value = "";
  respostas.value = [];
  try {
    for (let i = 0; i < perguntas.length; i++) {
      const p = perguntas[i];
      const alts = p.alternativas
        .map((a, j) => `Alternativa ${LETRAS[j].toUpperCase()}: ${a}`)
        .join(". ");

      status.value = "Lendo...";
      await falar(`Pergunta ${i + 1}. ${p.enunciado}. ${alts}`);

      status.value = "Ouvindo...";
      const fala = await ouvindoUsuario();
      const escolha = interpretar(fala, p.alternativas);

      respostas.value.push({ enunciado: p.enunciado, resposta: escolha ?? "" });
      await falar(escolha ? `Você escolheu ${escolha}` : "Não entendi, pulando.");
    }
    status.value = "Fim";
    await falar("Quiz finalizado!");
  } catch (e) {
    erro.value = (e as Error).message;
  }
}
</script>

<template>
  <div>
    <button @click="testarQuiz">Testar quiz por voz</button>
    <p>{{ status }}</p>
    <pre>{{ respostas }}</pre>
    <p v-if="erro">Erro: {{ erro }}</p>
  </div>
</template>