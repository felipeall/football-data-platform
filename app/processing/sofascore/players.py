import json
from dataclasses import dataclass

from app.models import sofascore
from app.processing.base import BaseProcessing


@dataclass
class SofascorePlayers(BaseProcessing):
    files_path: str = "files/sofascore/players/"

    def run(self):
        for data in self.files_data:
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
                dob=self.parse_timestamp(data_player.get("dateOfBirthTimestamp")),
                scrapped_at=self.parse_timestamp(data.get("scrapped_at")),
            )

            self.db.upsert_from_model(player)


def main():
    sofascore_players = SofascorePlayers()
    sofascore_players.run()


if __name__ == "__main__":
    main()
