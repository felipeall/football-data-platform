import json
from dataclasses import dataclass
from datetime import datetime, timezone

from app.models import sofascore
from app.processing.base import BaseProcessing


@dataclass
class SofascoreMatchesEvents(BaseProcessing):
    files_path: str = "files/sofascore/matches_events/"

    def run(self):
        for data in self.files_data:
            matches_events_data = json.loads(data["data"])
            teams_players = {
                data.get("metadata").get("home_team_id"): matches_events_data["home"]["players"],
                data.get("metadata").get("away_team_id"): matches_events_data["away"]["players"],
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
                        scrapped_at=datetime.fromtimestamp(data.get("scrapped_at"), tz=timezone.utc),
                    )
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
