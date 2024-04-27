import json
from dataclasses import dataclass
from datetime import datetime, timezone

from app.models import sofascore
from app.processing.base import BaseProcessing


@dataclass
class SofascoreTeams(BaseProcessing):
    files_path: str = "files/sofascore/teams"

    def run(self):
        for data in self.files_data:
            data_team = json.loads(data["data"])["team"]

            team = sofascore.SofascoreTeams(
                id=data_team["id"],
                name=data_team["name"],
                full_name=data_team["fullName"],
                country=data_team.get("country", {}).get("name")
                or data_team.get("primaryUniqueTournament").get("category").get("country").get("name"),
                country_code=data_team.get("country", {}).get("alpha2")
                or data_team.get("primaryUniqueTournament").get("category").get("country").get("alpha2"),
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
