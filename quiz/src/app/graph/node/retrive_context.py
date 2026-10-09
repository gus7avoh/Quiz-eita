
import logging

from typing import Any

from app.graph.state import QuizState
from infra.dto.google_drive_file_dto import GoogleDriveFileDTO
from infra.repository.google_drive_repository import GoogleDriveRepository
from infra.repository.rag_repository import RagRepository
from infra.repository.redis_client import RedisClient
from infra.llm.gemini_embedding_client import GeminiEmbeddingClient
from domain.entities.document_chunk import DocumentChunk
from infra.document.document_manager import DocumentManager


logger = logging.getLogger(__name__)


def load_document_content(
    google_drive: GoogleDriveRepository,
    document: GoogleDriveFileDTO,
) -> bytes:
    """Baixa o conteúdo bruto de um documento selecionado no Google Drive."""
    try:
        content = google_drive.get_file_content(document.file_id)
        return content
    except Exception:
        logger.exception(
            "Falha ao carregar documento do Google Drive file_id=%s",
            document.file_id,
        )
        raise


def create_chunks(text: str, chunk_size: int = 1000):
    try:
        return [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]
    except Exception:
        logger.exception("Falha ao dividir o texto em chunks")
        raise

async def make_embedded_context(
    gemini_embedding_client: GeminiEmbeddingClient,
    document: GoogleDriveFileDTO,
    content: bytes,
    document_manager: DocumentManager
) -> list[DocumentChunk]:
    """Transforma o conteúdo do documento em embedding e organiza seus metadados."""
    try:
        text = document_manager.extract_text(content, document.mime_type)

        chunks = create_chunks(text)

        vectors = await gemini_embedding_client.create_embedding(chunks)

        data = []
        for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
            data.append(
                DocumentChunk(
                    id_drive=document.file_id,
                    chunk=index,
                    name=document.name,
                    mime_type=document.mime_type,
                    date_modification=document.modified_time,
                    text=chunk,
                    embedding=vector
                )
            )

        return data

    except Exception:
        logger.exception(
            "Falha ao criar embeddings do documento file_id=%s",
            document.file_id,
        )
        raise

async def save_embedded_context(rag_repository: RagRepository, embedded_context: list[DocumentChunk]) -> None:
    """Salva no Redis o embedding, o conteúdo necessário e a versão do documento."""
    try:
        for document in embedded_context:
            
            logger.info(
                "Salvando embeddings no Redis para file_id=%s, chunk=%d",
                document.id_drive,
                document.chunk,
                document.name,
                document.embedding
            )
            await rag_repository.create(document)
            
    except Exception:
        logger.exception("Falha ao salvar embeddings no Redis")
        raise


async def update_cached(
    google_drive: GoogleDriveRepository,
    gemini_embedding_client: GeminiEmbeddingClient,
    rag_repository: RagRepository,
    document: GoogleDriveFileDTO,
    document_manager: DocumentManager
) -> bool:
    """Verifica no Redis se o documento é novo ou se foi alterado no Drive."""
    try:
        content = load_document_content(google_drive, document)
        embedded_context = await make_embedded_context(
            gemini_embedding_client,
            document,
            content,
            document_manager,
        )
        await save_embedded_context(rag_repository, embedded_context)

        return True
    except Exception:
        logger.exception(
            "Falha ao atualizar cache do documento file_id=%s",
            document.file_id,
        )
        raise


async def delete_cached(rag_repository: RagRepository, file_id: str) -> None:
    """Remove do Redis o embedding, o conteúdo necessário e a versão do documento."""
    try:
        await rag_repository.delete_document(file_id)
    except Exception:
        logger.exception(
            "Falha ao excluir cache do documento file_id=%s",
            file_id,
        )
        raise


async def verify_documents_state(document: GoogleDriveFileDTO, rag_repository: RagRepository) -> str:
    """Verifica se os documentos do Drive foram alterados, adicionados ou removidos em relação ao que está armazenado no Redis."""
    try:
        data = await rag_repository.get(document.file_id, 0)

        if data is None:
            return "insert"

        elif data and data.get("date_modification") != document.modified_time:
            return "update"

        return "none"
    except Exception:
        logger.exception(
            "Falha ao verificar estado do documento file_id=%s",
            document.file_id,
        )
        raise


async def syncronize_cache(
    google_drive: GoogleDriveRepository,
    rag_repository: RagRepository,
    gemini_embedding_client: GeminiEmbeddingClient,
    document_manager: DocumentManager
) -> None:
    """Sincroniza os documentos do Drive com os embeddings armazenados no Redis."""
    try:
        google_drive_files = google_drive.list_files()
        redis_files = await rag_repository.list_documents()
        google_drive_ids = {document.file_id for document in google_drive_files}

        for file_id in redis_files:
            if file_id not in google_drive_ids:
                await delete_cached(rag_repository, file_id)

        for document in google_drive_files:
            state = await verify_documents_state(document, rag_repository)
            if state == "update":
                await delete_cached(rag_repository, file_id)
                
            if state in ["update", "insert"]:
                await update_cached(
                    google_drive,
                    gemini_embedding_client,
                    rag_repository,
                    document,
                    document_manager,
                )
    except Exception:
        logger.exception("Falha ao sincronizar cache de documentos")
        raise



async def search_context_in_redis(rag_repository: RagRepository, state: QuizState) -> list[str]:
    """Busca no Redis os trechos mais relevantes para o tema atual do quiz."""
    try:
        tema = state.get("tema", "").strip().lower()
        context = await rag_repository.search_context(tema)
        return context
        
    except Exception:
        logger.exception("Falha ao buscar contexto no Redis")
        raise


async def retrive_context(state: QuizState) -> dict[str, Any]:
    """Atualiza a base de embeddings e devolve o contexto para o próximo nó do grafo."""
    try:
        google_drive = GoogleDriveRepository()

        redis_client = RedisClient("REDIS_URL_RAG")
        rag_repository = RagRepository(redis_client)

        gemini_embedding_client = GeminiEmbeddingClient(base_model="gemini-embedding-2")
        document_manager = DocumentManager(pdf_extractor=gemini_embedding_client)

        await syncronize_cache(
            google_drive,
            rag_repository,
            gemini_embedding_client,
            document_manager,
        )

        context = await search_context_in_redis(rag_repository, state)

        return {"context": context}
    except Exception:
        logger.exception("Falha no node retrieve_context")
        raise
