import re
from dataclasses import dataclass

import country_converter as cc
import countrynames as cn
import dateparser
from bs4 import BeautifulSoup
from tqdm import tqdm

from app.models import fbref
from app.services.aws import AWS
from app.services.db import Database


@dataclass
class FBrefPlayers:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/fbref/players"

    def run(self):
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
            soup = BeautifulSoup(data["data"], "lxml")

            name = soup.find("div", {"id": "meta"}).find("h1").get_text().strip()

            full_name = soup.find("div", {"id": "meta"}).find_all("p")[0].get_text()
            full_name = full_name if "Position" not in full_name else None

            dob = soup.find("div", {"id": "meta"}).find("a", {"href": re.compile("birthdays")})
            dob = dateparser.parse(dob.parent.get_text().strip()).date() if dob else None

            national_team = soup.find("div", {"id": "meta"}).find("a", {"href": re.compile("/country/")})
            national_team = national_team.get_text() if national_team else None

            born_in = soup.find("div", {"id": "meta"}).find("span", string=re.compile("in "))
            born_in = re.sub(r"^in\s", "", born_in.get_text().strip()) if born_in else None

            country_name = national_team or born_in

            team_url = soup.find("div", {"id": "meta"}).find("a", {"href": re.compile("/squads/")})
            team_id = (
                re.search(r"/squads/(?P<club_id>.+)/", team_url.get("href")).groupdict().get("club_id")
                if team_url
                else None
            )

            position = soup.find("div", {"id": "meta"}).find("strong", string=re.compile("Position"))
            position = position.next_sibling.text.replace("\xa0", "").replace("▪", "").strip() if position else None

            player = fbref.FBrefPlayers(
                id=data["id"],
                name=name,
                full_name=full_name,
                dob=dob,
                country_code=(
                    cn.to_code(country_name) or cc.convert(names=country_name, to="ISO2") if country_name else None
                ),
                country_name=country_name,
                team_id=team_id,
                position=position,
            )

            self.db.upsert_from_model(player)


def main():
    fbref_players = FBrefPlayers()
    fbref_players.run()


if __name__ == "__main__":
    main()
