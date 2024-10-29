import os

from tools.document_outputs.document_output_base import DocumentOutputBase
from tools.utils import html_to_pdf
from tools.logger_config import logger


class LocalFileOutput(DocumentOutputBase):
    def __init__(self, base_dir, file_name):
        self.base_dir = base_dir
        self.file_name = file_name

    def save(self, content, **_):
        output_file_name = os.path.join(self.base_dir, self.file_name)
        logger.info(f"writing PDF file {output_file_name}")
        html_to_pdf(content, output_file_name)
        return output_file_name
