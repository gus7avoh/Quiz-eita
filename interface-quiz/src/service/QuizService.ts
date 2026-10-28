import type { CriarQuizRequest, BuscarQuizResponse, RespostaRequest, DeletarRequest, Ranking, RespostaResponse } from '../types/QuizTypes'
import { usarMusicaFundo, usarEfeitoAudio } from '../composables/useBackgroundMusics';

// Empty by default means same-origin in production. Set VITE_API_URL only
// when the API is intentionally hosted on another origin.
const API_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')

//método de gerar quiz retornando um uuid em string
export async function criarQuiz(req: CriarQuizRequest): Promise<string> {

    const response = await fetch(`${API_URL}/quiz/create`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(req), 
    }) 

    if(!response.ok) throw new Error(`Erro ao criar quiz: ${response.status}`)
    
    const data = await response.json()
    if(!data?.uuid) throw new Error('Resposta sem uuid')
    return data.uuid
}

//método de procurar quiz usando uuid retornando BuscarQuizResponse ou null
export async function buscarQuiz(uuid: string): Promise<BuscarQuizResponse | null> {

    const response = await fetch(`${API_URL}/quiz/question`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({uuid}),
    })

    if(!response.ok) throw new Error(`Erro ao buscar perguntas: ${response.status}`)
    
    const data: BuscarQuizResponse| null = await response.json()
    return data?.perguntas && data.perguntas.length > 0 ? data : null
    //se data não for nulo, perguntas for um objeto válido e perguntas for maior que 0 
    // retorna data, se não null
}

//Método de enviar respostas usando uuid e uma lista de enunciados com alternatvias
export async function responderQuiz(request: RespostaRequest): Promise <RespostaResponse> {

    const response = await fetch(`${API_URL}/quiz/answer`, {

    method: 'POST',
    headers: { 'Content-Type' : 'application/json' },
    body: JSON.stringify({uuid: request.uuid, enunciado: request.enunciado, resposta_usuario: request.resposta_usuario}),
    })

    if(!response.ok) throw new Error(`Houve um erro ao enviar respostas: ${response.status}`)
    
    const data = await response.json()

    return data.resposta
}

//Método para excluir um quiz usando uuid
export async function deletarQuiz(request: DeletarRequest): Promise <boolean> {

    if(!request?.list_uuid?.length) {return false}

    const response = await fetch(`${API_URL}/quiz/` , {
        method: 'DELETE',
        headers: { 'Content-Type' : 'application/json' },
        body: JSON.stringify(request)
    })
    
    if(!response.ok) throw new Error(`Houve um erro ao excluir o quiz: ${response.status}`)
    
    const data = await response.json()
    
    return data.excluded
}
//Método para puxar todos os usuarios
export async function buscarUsuarios(): Promise <Ranking>{ 
    const response = await fetch(`${API_URL}/ranking`, {
        method: 'GET',
        headers: { 'Content-Type' : 'application/json' },
    })

    if(!response.ok) throw new Error(`Houve um erro ao buscar usuarios: ${response.status}`)
    
    const data = await response.json()
    
    return data
}

//Método para adicionar um usuario com pontuação no ranking
export async function adicionarUsuario(nome: string, pontos: number, dificuldade: string): Promise <boolean> {
    const response = await fetch(`${API_URL}/ranking`, {
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body: JSON.stringify({nome, pontos, dificuldade})
    })

    if(!response.ok) throw new Error(`Houve um erro ao adicionar usuario: ${response.status}`)
    
    const data = await response.json()
    
    return data.added
}

export async function mockadoBuscarusuarios(): Promise <Ranking>{
    return {
    'facil': [{nome: 'davi', pontos: 20}],
    'medio': [{nome: 'gustavo', pontos: 30}],
    'dificil': [{nome: 'matheus', pontos: 40}],
    'impossivel': [{nome: 'ana', pontos: 50}],
    'misto': [{nome: 'eduardo', pontos: 10}]
    }
}

const { iniciar, pausar, continuar, mudarVolume } = usarMusicaFundo()
export function comecarMusica(dificuldade: string) {
    iniciar(dificuldade)
}

export function pausarMusica() {
    pausar()
}

export function despausarMusica() {
    continuar()
}

export function mudarVolumeMusica(volume: number) {
    mudarVolume(volume)
}

const {usarEfeito} = usarEfeitoAudio()

export function efeitoAcertar() {
    usarEfeito(true)
}

export function efeitoErrar() {
    usarEfeito(false)
}
