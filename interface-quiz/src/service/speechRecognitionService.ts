async function garantirPermissaoMicrofone(): Promise<void> {
  if (!window.isSecureContext) {
    throw new Error("[ERROR] O microfone exige HTTPS ou localhost.");
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach((track) => track.stop()); 
  } catch {
    throw new Error("[ERROR] Permissão do microfone negada. Libere nas configurações dos eu navegador.");
  }
}


export async function ouvindoUsuario(lang: string = "pt-BR"): Promise<string> {
  await garantirPermissaoMicrofone();

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