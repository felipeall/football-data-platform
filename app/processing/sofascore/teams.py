import json
from dataclasses import dataclass
from datetime import datetime, timezone

from tqdm import tqdm

from app.models import sofascore
from app.services.aws import AWS
from app.services.db import Database


@dataclass
class SofascoreTeams:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/sofascore/teams"

    def run(self):
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
            data_team = json.loads(data["data"])["team"]

            team = sofascore.SofascoreTeams(
                id=data_team["id"],
                name=data_team["name"],
                full_name=data_team["fullName"],
                country=data_team["country"]["name"],
                country_code=data_team["country"]["alpha2"],
                league_id=data_team["primaryUniqueTournament"]["id"],
                league_name=data_team["primaryUniqueTournament"]["name"],
                scrapped_at=datetime.fromtimestamp(data.get("scrapped_at"), tz=timezone.utc),
            )

            self.db.upsert_from_model(team)


def main():
    sofascore_teams = SofascoreTeams()
    sofascore_teams.run()


if __name__ == "__main__":
    main()
