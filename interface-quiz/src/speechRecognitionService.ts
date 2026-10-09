export function ouvindoUsuario(lang: string = "pt-BR"): Promise<string> {
  return new Promise((resolve, reject) => {
    const Reconhecimento = window.SpeechRecognition ?? window.webkitSpeechRecognition;

    if (!Reconhecimento) {
      reject(new Error("Seu navegador não suporta reconhecimento de voz."));
      return;
    }

    const reconhecimento = new Reconhecimento();
    reconhecimento.lang = lang;
    reconhecimento.interimResults = false;

    reconhecimento.onresult = (event) => resolve(event.results[0][0].transcript);
    reconhecimento.onerror = (event) => reject(new Error(event.error));

    reconhecimento.start();
  });
}

export function falar(text: string, lang: string = "pt-BR"): Promise<void> {
  return new Promise((resolve, reject) => {
    const enunciado = new SpeechSynthesisUtterance(text);
    enunciado.lang = lang;
    enunciado.onend = () => resolve();
    enunciado.onerror = () => reject(new Error("Falha ao reproduzir o áudio."));
    window.speechSynthesis.speak(enunciado);
  });
}

type ResultadoResposta = {
  correto: boolean;
  respostaCorreta: string;
};

const URL_API = "http://localhost:5173/"; 

export async function enviarResposta(idQuestao: string, respostaUsuario: string,): Promise<ResultadoResposta> {
  const respostaServidor = await fetch(`${URL_API}/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idQuestao, respostaUsuario }),
  });
  
  if (!respostaServidor.ok) {
    throw new Error(`Erro do servidor: ${respostaServidor.status}`);
  }

  return respostaServidor.json();
}