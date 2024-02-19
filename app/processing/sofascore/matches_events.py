import json
from dataclasses import dataclass
from datetime import datetime, timezone

from tqdm import tqdm

from app.models import sofascore
from app.services.aws import AWS
from app.services.db import Database


@dataclass
class SofascoreMatchesEvents:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/sofascore/matches_events/"

    def run(self):
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
            matches_events_data = json.loads(data["data"])
            players = matches_events_data["home"]["players"] + matches_events_data["away"]["players"]

            for player in players:

                metadata = dict(
                    match_id=data.get("id"),
                    player_id=player.get("player").get("id"),
                    scrapped_at=datetime.fromtimestamp(data.get("scrapped_at"), tz=timezone.utc),
                )
                statistics = player.get("statistics")
                statistics = {self.camel_to_snake(k): v for k, v in self.flatten(statistics).items()}
                match_events = sofascore.SofascoreMatchesEvents(**metadata, **statistics)

                self.db.upsert_from_model(match_events)

    @staticmethod
    def camel_to_snake(name):
        return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")

    def flatten(self, d, parent_key="", sep="_"):
        items = {}
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            items.update({new_key: v} if not isinstance(v, dict) else self.flatten(v, new_key, sep))
        return items


def main():
    sofascore_matches_events = SofascoreMatchesEvents()
    sofascore_matches_events.run()


if __name__ == "__main__":
    main()
