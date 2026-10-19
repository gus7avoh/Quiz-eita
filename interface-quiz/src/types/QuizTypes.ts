export interface Pergunta {
    enunciado: string
    alternativas: string[]
} //como a api enxerga uma pergunta
    
export interface Resposta {
    enunciado: string
    resposta: string
}

export interface CriarQuizRequest {
    tema: string
    quantidade: number
    dificuldade: string
} //interace para criar um quiz

export interface BuscarQuizResponse {
    perguntas: Pergunta[]
} //interface para receber um quiz

export interface RespostaRequest{
    uuid: string
    enunciado: string
    resposta_usuario: string
}

export interface RespostaResponse {
    resposta: string
    correta: boolean
    explicacao: string
}

export interface Deletar{
    uuid: string
}

export interface DeletarRequest{
    list_uuid: Deletar[]
}

export interface Usuario{
    nome: string
    pontos: number
}

export interface Ranking {
    'facil': Usuario[]
    'medio': Usuario[]
    'dificil': Usuario[]
    'impossivel': Usuario[]
    'misto': Usuario[]
}

export const EnumQuizGame = {
    'respondendo': 'RESPONDENDO',
    'resultado': 'RESULTADO',
} as const

export type EstadoQuiz = (typeof EnumQuizGame)[keyof typeof EnumQuizGame]


