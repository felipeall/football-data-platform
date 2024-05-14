from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from tqdm import tqdm

from app.services.aws import AWS
from app.services.db import Database


@dataclass
class BaseProcessing:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = ""
    full_load: bool = True
    file_path: Optional[str] = None

    @property
    def files(self) -> list:
        if self.file_path:
            bucket_file_path = self.files_path + self.file_path
            return [bucket_file_path] if self.aws.file_exists(bucket_file_path) else []
        return self.aws.list_files(self.files_path)

    @property
    def files_data(self) -> iter:
        for file in (pbar := tqdm(self.files)):
            pbar.set_description(file)
            yield self.aws.read_from_json(file_path=file)

    @staticmethod
    def parse_timestamp(timestamp: Optional[int]) -> Optional[datetime]:
        if not timestamp:
            return None
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
