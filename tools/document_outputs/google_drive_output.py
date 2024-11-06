import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from tools.document_outputs.document_output_base import DocumentOutputBase
from tools.utils import html_to_pdf
from tools.logger_config import logger


SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class GoogleDriveOutput(DocumentOutputBase):
    def __init__(self, tmp_dir, file_name, parent_dir_id):
        self.tmp_dir = tmp_dir
        self.file_name = file_name
        self.parent_dir_id = parent_dir_id

    def save(self, content, **_):
        local_temp_file = os.path.join(self.tmp_dir, self.file_name)
        html_to_pdf(content, local_temp_file)

        drive_service = self._authenticate()

        duplicated_files = self._get_duplicated_files(drive_service)

        file_id = self._upload_file(drive_service, local_temp_file)

        self._delete_duplicated_files(drive_service, duplicated_files)

        self._grant_read_permission_to_everyone(drive_service, file_id)

        return f"https://drive.google.com/uc?id={file_id}"

    @staticmethod
    def _authenticate():
        creds = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"),
            scopes=SCOPES
        )

        return build("drive", "v3", credentials=creds)

    def _get_duplicated_files(self, drive_service):
        query = f"name='{self.file_name}' and mimeType='application/pdf' and '{self.parent_dir_id}' in parents"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])

    @staticmethod
    def _delete_duplicated_files(drive_service, files_to_delete) -> None:
        for item in files_to_delete:
            drive_service.files().delete(fileId=item['id']).execute()
            logger.info(f"Deleted duplicated file {item['name']} | id: {item['id']}")

    def _upload_file(self, drive_service, local_temp_file) -> str:
        file_metadata = {
            "name": self.file_name,
            "mimeType": "application/pdf",
            "parents": [self.parent_dir_id]
        }

        media = MediaFileUpload(local_temp_file, mimetype='application/pdf')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logger.info(f"Uploaded file {self.file_name} ID: {file.get('id')}")

        return file["id"]

    @staticmethod
    def _grant_read_permission_to_everyone(drive_service, file_id) -> None:
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        drive_service.permissions().create(fileId=file_id, body=permission).execute()
        logger.debug(f"granted read permission to anyone for file: {file_id}")
