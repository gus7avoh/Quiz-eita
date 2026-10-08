from io import BytesIO
from pypdf import PdfReader

class DocumentManager:

    def __init__(self, pdf_extractor):
        self.pdf_extractor = pdf_extractor

    def extract_text(self, content: bytes, mime_type: str) -> str:
        if not mime_type == "application/pdf":
            raise ValueError("Tipo de documento não suportado")
        
        reader = PdfReader(BytesIO(content))

        return "\n".join(
            page.extract_text(extraction_mode="layout") or ""
            for page in reader.pages
        )