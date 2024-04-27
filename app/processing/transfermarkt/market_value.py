import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from app.models import transfermarkt
from app.processing.base import BaseProcessing


@dataclass
class TransfermarktMarketValue(BaseProcessing):
    files_path: str = "files/transfermarkt/market_value/"

    def run(self):
        for data in self.files_data:
            data_mv = json.loads(data["data"])

            club_image_url = None
            for entry in data_mv["list"]:
                if entry.get("wappen"):
                    club_image_url = entry["wappen"]
                entry["wappen"] = club_image_url

                transfermarkt_mv = transfermarkt.TransfermarktMarketValue(
                    player_id=data["id"],
                    club_id=re.search(r"(?P<club_id>\d+)", entry["wappen"]).group("club_id"),
                    date=entry["datum_mw"],
                    age=entry["age"],
                    value=entry["y"],
                    scrapped_at=datetime.fromtimestamp(data["scrapped_at"], tz=timezone.utc),
                )

                self.db.upsert_from_model(transfermarkt_mv)


def main():
    transfermarkt_market_value = TransfermarktMarketValue()
    transfermarkt_market_value.run()


if __name__ == "__main__":
    main()
