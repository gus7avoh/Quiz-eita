class GoogleDriveFileDTO:
    def __init__(self, file_id, name, mime_type, modified_time):
        self.file_id = file_id
        self.name = name
        self.mime_type = mime_type
        self.modified_time = modified_time