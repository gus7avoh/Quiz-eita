export function listenOnce(lang: string = "pt-BR"): Promise<string> {
  return new Promise((resolve, reject) => {
    const Recognition = window.SpeechRecognition ?? window.webkitSpeechRecognition;

    if (!Recognition) {
      reject(new Error("[ERROR] - Seu navegador não suporta reconhecimento de voz!"));
      return;
    }

    const recognition = new Recognition();
    recognition.lang = lang;
    recognition.interimResults = false;

    recognition.onresult = (event) => resolve(event.results[0][0].transcript);
    recognition.onerror = (event) => reject(new Error(event.error));

    recognition.start();
  });
}