import type { CriarQuizRequest, BuscarQuizResponse } from '../types/QuizTypes'

const API_URL = 'http://127.0.0.1:8000'

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