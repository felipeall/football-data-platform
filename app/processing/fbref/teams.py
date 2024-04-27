import re
from dataclasses import dataclass
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from app.models import fbref
from app.processing.base import BaseProcessing


@dataclass
class FBrefTeams(BaseProcessing):
    files_path: str = "files/fbref/teams"

    def run(self):
        for data in self.files_data:
            soup = BeautifulSoup(data["data"], "lxml")

            team_name = soup.find("div", {"id": "meta"}).find("h1").get_text().strip()
            team_name = re.search(r"[\d-]+[\s](?P<team_name>.+) Stats", team_name).groupdict().get("team_name")

            country = soup.find("div", {"id": "meta"}).find("a", {"href": re.compile("/country/")}).get_text()

            league_name = soup.find("div", {"id": "meta"}).find("strong", string="Record:").parent.find("a").get_text()
            league_url = soup.find("div", {"id": "meta"}).find("strong", string="Record:").parent.find("a").get("href")

            team = fbref.FBrefTeams(
                id=data["id"],
                name=team_name,
                country=country,
                league_name=league_name,
                league_url=league_url,
                scrapped_at=datetime.fromtimestamp(data["scrapped_at"], tz=timezone.utc),
            )

            self.db.upsert_from_model(team)


def main():
    fbref_teams = FBrefTeams()
    fbref_teams.run()


if __name__ == "__main__":
    main()
