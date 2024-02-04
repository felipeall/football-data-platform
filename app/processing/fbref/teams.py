import re
from dataclasses import dataclass

from bs4 import BeautifulSoup
from tqdm import tqdm

from app.models import fbref
from app.services.aws import AWS
from app.services.db import Database


@dataclass
class FBrefTeams:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/fbref/teams"

    def run(self):
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
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
            )

            self.db.load_dict(data=team.to_dict(), table="teams", schema="fbref")


def main():
    fbref_teams = FBrefTeams()
    fbref_teams.run()


if __name__ == "__main__":
    main()
