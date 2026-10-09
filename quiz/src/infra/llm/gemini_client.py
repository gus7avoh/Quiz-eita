from langchain_google_genai import ChatGoogleGenerativeAI
from infra.llm.key_manager import GeminiKeyManager
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class GeminiClient:
    
    def __init__(self):
        self.key_manager = GeminiKeyManager()
        self.base_model = "gemini-3.5-flash-lite"

    def invoke(self, prompt, structured_output=None):
        for _ in range(len(self.key_manager.keys)):
            api_key = self.key_manager.get_key()
            llm = self.create_llm(api_key, self.base_model)

            if structured_output:
               llm = llm.with_structured_output(structured_output)

            try:
                result = llm.invoke(prompt)
                self.key_manager.switched = False
                return result

            except Exception as error:
                print(f"Chave falhou: {error}")
                status_code = getattr(error, "status_code", None)
                if status_code == 429:
                    if self.key_manager.switched:
                        raise Exception("Todas as API Keys foram utilizadas")
                    self.key_manager.next_key()
                    return self.invoke(prompt)
                raise

        raise Exception("Internal Server Error", 500)


    @staticmethod
    def create_llm(api_key: str , base_model: str):
        return ChatGoogleGenerativeAI(
            model=base_model,
            google_api_key=api_key,
        )

