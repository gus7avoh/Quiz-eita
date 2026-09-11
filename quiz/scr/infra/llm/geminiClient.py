from langchain_google_genai import ChatGoogleGenerativeAI
from infra.llm.key_manager import GeminiKeyManager


class GeminiClient:

    def __init__(self, structured_output=None):
        self.key_manager = GeminiKeyManager()
        self.structured_output = structured_output

    def invoke(self, prompt):
        for _ in range(len(self.key_manager.keys)):
            api_key = self.key_manager.get_key()
            llm = self.create_llm(api_key)

            if self.is_structured_output():
               llm = llm.with_structured_output(self.structured_output)

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

        raise Exception("Internal Server Error", 500)

    def is_structured_output(self):
        if self.structured_output:
            return True
        return False

    @staticmethod
    def create_llm(api_key: str):
        return ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=api_key,
        )
