import json
from dataclasses import dataclass
from datetime import datetime, timezone

from tqdm import tqdm

from app.models import sofascore
from app.services.aws import AWS
from app.services.db import Database


@dataclass
class SofascorePlayers:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/sofascore/players"

    def run(self):
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
            data_player: dict = json.loads(data["data"])["player"]

            player = sofascore.SofascorePlayers(
                id=data_player.get("id"),
                name=data_player.get("name"),
                short_name=data_player.get("shortName"),
                team_id=data_player.get("team").get("id"),
                position=data_player.get("position"),
                jersey_number=data_player.get("jerseyNumber"),
                height=data_player.get("height"),
                preferred_foot=data_player.get("preferredFoot"),
                retired=data_player.get("retired"),
                country_code=data_player.get("country").get("alpha2"),
                country_name=data_player.get("country").get("name"),
                dob=(
                    datetime.fromtimestamp(data_player.get("dateOfBirthTimestamp"), tz=timezone.utc)
                    if data_player.get("dateOfBirthTimestamp")
                    else None
                ),
            )

            self.db.upsert_from_model(player)


def main():
    sofascore_players = SofascorePlayers()
    sofascore_players.run()


if __name__ == "__main__":
    main()
