import { ref } from 'vue';

const audio = new Audio
audio.loop = true
audio.volume = 1

const tocando = ref(false)

const efeito = new Audio()
efeito.loop = false
efeito.volume=1
export function usarMusicaFundo() {
    function iniciar(musica: string) {
        switch(musica) {

            case'Fácil':
                audio.src = '/musicas/musicaFacil.mp3'
            break

            case 'Médio':
                audio.src = '/musicas/musicaMedio.mp3'
            break

            case 'Difícil':
                audio.src = '/musicas/musicaDificil.mp3'
            break

            case 'Impossível':
                audio.src = '/musicas/musicaImpossivel.mp3'
            break

            case 'Misto':
                audio.src = '/musicas/musicaMisto.mp3'
            break
        }
        audio.play().then(() => (tocando.value = true))
    }    

    function pausar() {
        audio.pause()
        tocando.value=false
    }
    function mudarVolume(volume: number) {
        audio.volume=volume
    }
    function continuar() {
        audio.play()
    }
    return { iniciar, pausar, continuar, tocando }
}

export function usarEfeitoAudio() {
    function usarEfeito(acerto: boolean) {
        acerto ? efeito.src = '/efeitos/acertei.mp3' : efeito.src = '/efeitos/errei.mp3'
        efeito.play()
    }
    return { usarEfeito }
}

