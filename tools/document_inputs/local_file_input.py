import os

from tools.document_inputs.document_input_base import DocumentInputBase
from tools.logger_config import logger


class LocalFileInput(DocumentInputBase):
    def __init__(self, base_dir, file_name):
        self.base_dir = base_dir
        self.file_name = file_name

    def read(self, **_):
        file_path = os.path.join(self.base_dir, self.file_name)
        logger.debug(f"reading file {file_path}")
        with open(file_path) as f:
            return f.read()
