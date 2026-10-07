from infra.llm.key_manager import GeminiKeyManager
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class GeminiEmbeddingClient:
    
    def __init__(self):
        self.key_manager = GeminiKeyManager()
        self.base_model = "gemini-embedding-2"

    async def embed_documents(self, chunk: list[str]) -> list[list[float]]:
        for _ in range(len(self.key_manager.keys)):
            api_key = self.key_manager.get_key()
            llm = self.create_llm(api_key, self.base_model)

            try:
                result = await self.make_embedding_list(llm, chunk)
                self.key_manager.switched = False
                return result

            except Exception as error:
                print(f"Chave falhou: {error}")
                status_code = getattr(error, "status_code", None)
                if status_code == 429:
                    if self.key_manager.switched:
                        raise Exception("Todas as API Keys foram utilizadas")
                    self.key_manager.next_key()
                    return await self.make_embedding_list(llm, chunk)
                raise

        raise Exception("Internal Server Error", 500)
    
    
    async def make_embedding_list(self, llm: GoogleGenerativeAIEmbeddings, chunk_list: list[str]) -> list[list[float]]:
        results = []
        for chunk in chunk_list:
            results.append(await llm.aembed_query(chunk))
        return results


    @staticmethod
    def create_llm(api_key: str , base_model: str) -> GoogleGenerativeAIEmbeddings:
        return GoogleGenerativeAIEmbeddings(
            model=base_model,
            google_api_key=api_key,
        )

