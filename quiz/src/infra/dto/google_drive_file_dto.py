class GoogleDriveFileDTO:
    def __init__(self, id, name, mimeType, modifiedTime):
        self.file_id = id
        self.name = name
        self.mime_type = mimeType
        self.modified_time = modifiedTime