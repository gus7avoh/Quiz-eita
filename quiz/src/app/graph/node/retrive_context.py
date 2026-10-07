
from typing import Any

from app.graph.state import QuizState
from infra.dto.google_drive_file_dto import GoogleDriveFileDTO
from infra.repository.google_drive_repository import GoogleDriveRepository
from infra.repository.rag_repository import RagRepository
from infra.repository.redis_client import RedisClient
from infra.llm.gemini_embedding_client import GeminiEmbeddingClient
from domain.entities.document_chunk import DocumentChunk
from quiz.src.infra.document.document_manager import DocumentManager


def load_document_content(
    google_drive: GoogleDriveRepository,
    document: GoogleDriveFileDTO,
) -> bytes:
    """Baixa o conteúdo bruto de um documento selecionado no Google Drive."""
    content = google_drive.get_file_content(document.file_id)
    return content


def create_chunks(text: str, chunk_size: int = 1000):
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]
    

def make_embedded_context(
    gemini_embedding_client: GeminiEmbeddingClient,
    document: GoogleDriveFileDTO,
    content: bytes,
    document_manager: DocumentManager
) -> dict[str, Any]:
    """Transforma o conteúdo do documento em embedding e organiza seus metadados."""
    
    text = document_manager.extract_text(content, document.mime_type)

    chunks = create_chunks(text)

    vectors = gemini_embedding_client.embed_documents(chunks)

    data = []
    for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
        data.append(
            DocumentChunk(
                id_drive=document.file_id,
                chunk=index,
                name=document.name,
                document_type=document.mime_type, # precisar ser ex python, preciso implementar a função de extração
                date_modification=document.modified_time,
                text=chunk,
                embedding=vector
            )
        )


def save_embedded_context(rag_repository: RagRepository, embedded_context: dict[str, Any]) -> None:
    """Salva no Redis o embedding, o conteúdo necessário e a versão do documento."""
    pass


async def update_cached(
    google_drive: GoogleDriveRepository,
    gemini_embedding_client: GeminiEmbeddingClient,
    rag_repository: RagRepository,
    document: GoogleDriveFileDTO,
    document_manager: DocumentManager
) -> bool:
    """Verifica no Redis se o documento é novo ou se foi alterado no Drive."""
    content = load_document_content(google_drive, document)
    embedded_context = make_embedded_context(gemini_embedding_client, document, content, document_manager)
    save_embedded_context(rag_repository, embedded_context)
    
    return True


async def delete_cached(rag_repository: RagRepository, file_id: str) -> None:
    """Remove do Redis o embedding, o conteúdo necessário e a versão do documento."""
    await rag_repository.delete_document(file_id)


async def verify_documents_state(document: GoogleDriveFileDTO, rag_repository: RagRepository) -> str:
    """Verifica se os documentos do Drive foram alterados, adicionados ou removidos em relação ao que está armazenado no Redis."""
    
    data = await rag_repository.get(document.file_id, 0)
    
    if data is None:
        return "update"
    
    elif data and data.get("date_modification") != document.modified_time:
        return "update"
    
    return "none"


async def syncronize_cache(
    google_drive: GoogleDriveRepository,
    rag_repository: RagRepository,
    gemini_embedding_client: GeminiEmbeddingClient,
    document_manager: DocumentManager
) -> None:
    """Sincroniza os documentos do Drive com os embeddings armazenados no Redis."""
    
    google_drive_files = google_drive.list_files()
    redis_files = await rag_repository.list_documents()
    google_drive_ids = {document.file_id for document in google_drive_files}
    
    for file_id in redis_files:
        if file_id not in google_drive_ids:
            await delete_cached(rag_repository, file_id)
    
    for document in google_drive_files:
        state = await verify_documents_state(document, rag_repository)
        if (state == "update"):
            await update_cached(google_drive, gemini_embedding_client, rag_repository, document, document_manager)



def search_context_in_redis(state: QuizState) -> list[str]:
    """Busca no Redis os trechos mais relevantes para o tema atual do quiz."""
    pass


async def retrieve_context(state: QuizState) -> dict[str, Any]:
    """Atualiza a base de embeddings e devolve o contexto para o próximo nó do grafo."""
    google_drive = GoogleDriveRepository()
    
    redis_client = RedisClient("REDIS_URL_RAG")
    rag_repository = RagRepository(redis_client)
    
    gemini_embedding_client = GeminiEmbeddingClient(base_model="gemini-embedding-2")
    documente_manager = DocumentManager(pdf_extractor=gemini_embedding_client)
    
    await syncronize_cache(google_drive, rag_repository, gemini_embedding_client, documente_manager)
    
    context = search_context_in_redis(state)
    
    state.set("context", context)
    
    
            
