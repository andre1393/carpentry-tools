import os
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from tools.document_inputs.document_input_base import DocumentInputBase
from tools.logger_config import logger


SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class GoogleDriveInput(DocumentInputBase):

    def __init__(self, doc_id):
        self.doc_id = doc_id

    def read(self, **_):

        drive_service = self._authenticate()

        file_name = self._get_file_name(drive_service)
        local_file_name = os.path.join("/tmp", file_name)

        if not Path(local_file_name).exists():
            logger.info(f"{local_file_name} doesn't exists yet locally. Downloading it...")
            self._download_file(drive_service, local_file_name)
        else:
            logger.info(f"{local_file_name} already exists locally. Skipping download.")

        content = self._read_file(local_file_name)
        return content

    @staticmethod
    def _read_file(file_name):
        with open(file_name, "r") as f:
            return f.read()

    def _get_file_name(self, drive_service):
        return drive_service.files().get(fileId=self.doc_id, fields="name, mimeType").execute()["name"]

    @staticmethod
    def _authenticate():
        creds = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"),
            scopes=SCOPES
        )

        drive_service = build("drive", "v3", credentials=creds)
        return drive_service

    def _download_file(self, drive_service, local_file_name):
        request = drive_service.files().get_media(fileId=self.doc_id)
        with open(local_file_name, "wb") as temp_file:
            downloader = MediaIoBaseDownload(temp_file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                logger.debug(f"Download {int(status.progress() * 100)}%.")
