from dataclasses import dataclass

from tqdm import tqdm

from app.services.aws import AWS
from app.services.db import Database


@dataclass
class BaseProcessing:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = ""

    @property
    def files(self):
        return self.aws.list_files(self.files_path)

    @property
    def files_data(self):
        for file in (pbar := tqdm(self.files)):
            pbar.set_description(file)
            yield self.aws.read_from_json(file_path=file)
