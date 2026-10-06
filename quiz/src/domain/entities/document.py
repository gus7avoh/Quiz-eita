class Document:
    def __init__(
        self,
        id_drive,
        name,
        type,
        content,
        date_modification
    ):
        self.id_drive = id_drive
        self.name = name
        self.type = type
        self.content = content
        self.date_modification = date_modification