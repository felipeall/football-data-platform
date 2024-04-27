import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from tqdm import tqdm

from app.models import transfermarkt
from app.services.aws import AWS
from app.services.db import Database


@dataclass
class TransfermarktMarketValue:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/transfermarkt/market_value/"

    def run(self):
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
            data_mv = json.loads(data["data"])

            club_image_url = None
            for entry in data_mv["list"]:
                entry["wappen"] = entry.get("wappen", club_image_url)
                club_image_url = entry["wappen"]
                transfermarkt_mv = transfermarkt.TransfermarktMarketValue(
                    player_id=data["id"],
                    club_id=self.safe_regex(entry["wappen"], r"(?P<club_id>\d+)", "club_id"),
                    date=entry["datum_mw"],
                    age=entry["age"],
                    value=entry["y"],
                    scrapped_at=datetime.fromtimestamp(data["scrapped_at"], tz=timezone.utc),
                )
                self.db.upsert_from_model(transfermarkt_mv)

    @staticmethod
    def trim(text):
        if isinstance(text, list):
            text = "".join(text)

        return text.strip().replace("\xa0", "")

    def safe_regex(self, text, regex, group):
        if not isinstance(text, (str, list)) or not text:
            return None

        try:
            groups = re.search(regex, self.trim(text)).groupdict()
            return groups.get(group)
        except AttributeError:
            return None


def main():
    transfermarkt_market_value = TransfermarktMarketValue()
    transfermarkt_market_value.run()


if __name__ == "__main__":
    main()
