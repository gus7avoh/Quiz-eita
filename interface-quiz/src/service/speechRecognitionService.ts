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

interface SessaoReconhecimento {
  reconhecimento: SpeechRecognition | null
  cancelada: boolean
  finalizada: boolean
  resolver: (texto: string) => void
  rejeitar: (erro: Error) => void
}

let sessaoAtual: SessaoReconhecimento | null = null

export async function ouvindoUsuario(lang: string = "pt-BR"): Promise<string> {
  return new Promise((resolver, rejeitar) => {
    const sessao: SessaoReconhecimento = {
      reconhecimento: null,
      cancelada: false,
      finalizada: false,
      resolver,
      rejeitar,
    }
    sessaoAtual = sessao
    void iniciarReconhecimento(sessao, lang)
  })
}

function finalizarSessao(
  sessao: SessaoReconhecimento,
  texto?: string,
  erro?: Error,
) {
  if (sessao.finalizada) return

  sessao.finalizada = true
  if (sessaoAtual === sessao) sessaoAtual = null

  if (erro) sessao.rejeitar(erro)
  else sessao.resolver(texto ?? "")
}

async function iniciarReconhecimento(
  sessao: SessaoReconhecimento,
  lang: string,
) {
  try {
    await garantirPermissaoMicrofone()
    if (sessao.cancelada) {
      finalizarSessao(sessao)
      return
    }

    const Reconhecimento = window.SpeechRecognition ?? window.webkitSpeechRecognition;
    if (!Reconhecimento) {
      throw new Error("Seu navegador não suporta reconhecimento de voz.")
    }

    const reconhecimento = new Reconhecimento()
    sessao.reconhecimento = reconhecimento
    reconhecimento.lang = lang
    reconhecimento.interimResults = false
    let texto = ""

    reconhecimento.onresult = (event) => {
      texto = event.results[0][0].transcript
    }
    reconhecimento.onerror = (event) => {
      if (!sessao.cancelada) {
        finalizarSessao(sessao, undefined, new Error(event.error))
      }
    }
    reconhecimento.onend = () => {
      finalizarSessao(sessao, sessao.cancelada ? "" : texto)
    }

    if (sessao.cancelada) {
      finalizarSessao(sessao)
      return;
    }

    reconhecimento.start()
  } catch (erro) {
    finalizarSessao(
      sessao,
      undefined,
      erro instanceof Error ? erro : new Error(String(erro)),
    )
  }
}

export function pararOuvir() {
  const sessao = sessaoAtual
  if (!sessao) return

  sessao.cancelada = true
  if (!sessao.reconhecimento) {
    finalizarSessao(sessao)
    return
  }

  try {
    sessao.reconhecimento.stop()
  } catch (erro) {
    console.error("Não foi possível parar o reconhecimento de voz.", erro)
    finalizarSessao(sessao)
  }
}

 export async function falar(text: string, lang: string = "pt-BR"): Promise<void> {
  return new Promise((resolve, reject) => {
    const enunciado = new SpeechSynthesisUtterance(text);
    enunciado.lang = lang;
    enunciado.onend = () => resolve();
    enunciado.onerror = () => reject(new Error("Falha ao reproduzir o áudio."));
    window.speechSynthesis.speak(enunciado);
  });
}