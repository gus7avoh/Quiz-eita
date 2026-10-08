
from infra.repository.google_drive_cllient import GoogleDriveClient
from infra.dto.google_drive_file_dto import GoogleDriveFileDTO


class GoogleDriveRepository:
    def __init__(self):
        self.client = GoogleDriveClient()
        
    def list_files(self):
        response = (
            self.client.service.files()
            .list(
                q=f"'{self.client.FODER_ID}' in parents and trashed = false",
                fields="files(id, name, mimeType, modifiedTime)"
            )
            .execute()
        )

        result =  response.get("files", [])
        return [GoogleDriveFileDTO(**file_info) for file_info in result]
    
    
    def get_file_content(self, file_id):
        response = (
            self.client.service.files()
            .get_media(fileId=file_id)
            .execute()
        )
        return response

