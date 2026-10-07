class DocumentChunk:
    def __init__(
        self,
        id_drive,
        chunk,
        name,
        document_type,
        date_modification,
        text,
        embedding
    ):
        self.id_drive = id_drive
        self.chunk = chunk
        self.name = name
        self.document_type = document_type
        self.date_modification = date_modification
        self.text = text
        self.embedding = embedding