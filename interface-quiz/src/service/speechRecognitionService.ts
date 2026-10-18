export async function garantirPermissaoMicrofone(): Promise<void> {
  if (!window.isSecureContext) {
    throw new Error("O microfone exige HTTPS ou localhost.");
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach((t) => t.stop());
  } catch {
    throw new Error("Permissão do microfone negada. Libere nas configurações do navegador.");
  }
}

export function ouvindoUsuario(lang = "pt-BR"): Promise<string> {
  return new Promise((resolve, reject) => {
    const Reconhecimento = window.SpeechRecognition ?? window.webkitSpeechRecognition;
    if (!Reconhecimento) {
      reject(new Error("Seu navegador não suporta reconhecimento de voz."));
      return;
    }

    const r = new Reconhecimento();
    r.lang = lang;
    r.interimResults = false;
    r.maxAlternatives = 1;

    let resolvido = false;

    r.onresult = (event: any) => {
      resolvido = true;
      resolve(event.results[0][0].transcript);
    };
    r.onerror = (event: any) => {
      resolvido = true;
      reject(new Error(event.error));
    };
    r.onend = () => {
    
      if (!resolvido) resolve("");
    };

    r.start();
  });
}

export function falar(text: string, lang = "pt-BR"): Promise<void> {
  return new Promise((resolve, reject) => {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = lang;
    u.onend = () => resolve();
    u.onerror = () => reject(new Error("Falha ao reproduzir o áudio."));
    window.speechSynthesis.speak(u);
  });
}

type ResultadoResposta = { correto: boolean; respostaCorreta: string };

const URL_API = "http://169.58.5.68:8000";

export async function enviarResposta(
  idQuestao: string,
  respostaUsuario: string
): Promise<ResultadoResposta> {
  const res = await fetch(`${URL_API}/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idQuestao, respostaUsuario }),
  });
  if (!res.ok) throw new Error(`Erro do servidor: ${res.status}`);
  return res.json();
}