from google.oauth2 import service_account
from googleapiclient.discovery import build
import dotenv
import os

class GoogleDriveClient:
    
    dotenv.load_dotenv()

    SCOPES = [
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    FODER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    
    GOOGLE_DRIVE_CREDENTIALS_NAME= os.getenv("GOOGLE_DRIVE_CREDENTIALS_NAME")
    
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
    )

    GOOGLE_DRIVE_CREDENTIALS_PATH = os.path.join(
        BASE_DIR,
        GOOGLE_DRIVE_CREDENTIALS_NAME
    )

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.GOOGLE_DRIVE_CREDENTIALS_PATH,
            scopes=self.SCOPES
        )

        self.service = build(
            "drive",
            "v3",
            credentials=credentials
        )

    def list_files(self):
        response = (
            self.service.files()
            .list(
                q=f"'{self.FODER_ID}' in parents and trashed = false",
                fields="files(id, name, mimeType, modifiedTime)"
            )
            .execute()
        )

        return response.get("files", [])
    
    
    
    
drive =  GoogleDriveClient()
print(drive.list_files())