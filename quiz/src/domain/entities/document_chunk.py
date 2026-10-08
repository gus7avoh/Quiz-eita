class DocumentChunk:
    def __init__(
        self,
        id_drive,
        chunk,
        name,
        mime_type,
        date_modification,
        text,
        embedding
    ):
        self.id_drive = id_drive
        self.chunk = chunk
        self.name = name
        self.mime_type = mime_type
        self.document_type = self.find_document_type()
        self.date_modification = date_modification
        self.text = text
        self.embedding = embedding
        
    
    def find_document_type(self):
        name_split = self.name.split('-')
        if len(name_split) > 1:
            return name_split[0].strip()
        else:
            raise ValueError("O nome do documento não contém um tipo de documento válido.")
            