import json
import logging
from dataclasses import dataclass

import boto3
from botocore.client import BaseClient

from app.settings import settings

logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
log = logging.getLogger(__name__)


@dataclass
class AWS:
    def __post_init__(self):
        log.debug("Initializing AWS client...")
        self.client: BaseClient = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL,
        )
        log.debug("Initialized AWS client!")

    def save_to_json(self, data: dict, path: str, file_name: str):
        log.debug(f"Saving {file_name}.json @ {path}")
        self.client.put_object(Body=json.dumps(data), Bucket=settings.AWS_BUCKET_NAME, Key=f"{path}/{file_name}.json")

    def read_from_json(self, file_path: str) -> dict:
        return json.loads(
            self.client.get_object(Bucket=settings.AWS_BUCKET_NAME, Key=file_path).get("Body").read().decode("utf-8"),
        )

    def count_files(self, path: str) -> int:
        return len(self.client.list_objects(Bucket=settings.AWS_BUCKET_NAME, Prefix=path).get("Contents", []))

    def list_files(self, path: str) -> list:
        return [
            i.get("Key")
            for i in self.client.list_objects(Bucket=settings.AWS_BUCKET_NAME, Prefix=path).get("Contents", [])
        ]
