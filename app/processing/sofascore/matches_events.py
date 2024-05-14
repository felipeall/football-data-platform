import json
from dataclasses import dataclass

from app.models import sofascore
from app.processing.base import BaseProcessing


@dataclass
class SofascoreMatchesEvents(BaseProcessing):
    files_path: str = "files/sofascore/matches_events/"

    def run(self):
        latest_scrapped_at = self.db.get_latest_scrapped_at(sofascore.SofascoreMatchesEvents())

        for data in self.files_data:
            scrapped_at = self.parse_timestamp(data.get("scrapped_at"))
            data_matches_events = json.loads(data["data"])
            teams_players = {
                data.get("metadata").get("home_team_id"): data_matches_events["home"]["players"],
                data.get("metadata").get("away_team_id"): data_matches_events["away"]["players"],
            }

            for team_id, team_players in teams_players.items():
                for player in team_players:
                    statistics = player.get("statistics", {})
                    statistics = {self.camel_to_snake(k): v for k, v in self.flatten(statistics).items()}
                    metadata = dict(
                        match_id=data.get("id"),
                        player_id=player.get("player").get("id"),
                        team_id=team_id,
                        has_statistics=bool(statistics),
                        scrapped_at=scrapped_at,
                    )
                    match_events = sofascore.SofascoreMatchesEvents(**metadata, **statistics)
                    if player.get("player").get("name") == "Lionel Messi":
                        print(match_events)

                    if self.full_load or scrapped_at > latest_scrapped_at:
                        self.db.upsert_from_model(match_events)

    @staticmethod
    def camel_to_snake(name: str) -> str:
        return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")

    def flatten(self, d: dict, parent_key: str = "", sep: str = "_") -> dict:
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
