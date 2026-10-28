import type { CriarQuizRequest, BuscarQuizResponse, RespostaRequest, DeletarRequest, Ranking, RespostaResponse, Usuario } from '../types/QuizTypes'
import { usarMusicaFundo, usarEfeitoAudio } from '../composables/useBackgroundMusics';

// In production the API and the compiled frontend are served by the same
// origin. A separate URL is only needed when the API is hosted elsewhere.
// Keep the localhost fallback for the Vite development server so local work
// continues to reach an API running on port 8000 without extra configuration.
const configuredApiUrl = import.meta.env.VITE_API_URL
const API_URL = (configuredApiUrl ?? (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '')).replace(/\/$/, '')

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
const dificuldadesRanking = {
    facil: 'Fácil',
    medio: 'Médio',
    dificil: 'Difícil',
    impossivel: 'Impossível',
    misto: 'Misto',
} as const

export type DificuldadeRanking = keyof typeof dificuldadesRanking

export async function buscarRanking(dificuldade: string): Promise<Usuario[]> {
    const response = await fetch(`${API_URL}/ranking/${encodeURIComponent(dificuldade)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })

    if(!response.ok) throw new Error(`Houve um erro ao buscar o ranking: ${response.status}`)

    const data: { ranking?: Usuario[] } = await response.json()
    return data.ranking ?? []
}

export async function buscarUsuarios(): Promise<Ranking>{
    const entradas = Object.entries(dificuldadesRanking) as [DificuldadeRanking, string][]
    const resultados = await Promise.all(
        entradas.map(async ([chave, dificuldade]) => [chave, await buscarRanking(dificuldade)] as const),
    )

    const ranking = {} as Ranking
    for (const [chave, lista] of resultados) {
        ranking[chave] = lista
    }
    return ranking
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

const { iniciar, pausar, continuar, mudarVolume } = usarMusicaFundo()
export function comecarMusica(dificuldade: string): Promise<void> {
    return iniciar(dificuldade)
}

export function pausarMusica() {
    pausar()
}

export function despausarMusica(): Promise<void> {
    return continuar()
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
