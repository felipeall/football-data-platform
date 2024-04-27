import json
from dataclasses import dataclass
from datetime import datetime, timezone

from tqdm import tqdm

from app.models import sofascore
from app.services.aws import AWS
from app.services.db import Database


@dataclass
class SofascoreMatches:
    aws: AWS = AWS()
    db: Database = Database()
    files_path: str = "files/sofascore/matches/"

    def run(self):
        files = self.aws.list_files(self.files_path)

        for file in (pbar := tqdm(files)):
            pbar.set_description(file)
            data = self.aws.read_from_json(file_path=file)
            data_match: dict = json.loads(data["data"])

            for event in data_match.get("events"):

                tournament = sofascore.SofascoreTournaments(
                    id=event.get("tournament").get("uniqueTournament").get("id"),
                    name=event.get("tournament").get("uniqueTournament").get("name"),
                    slug=event.get("tournament").get("uniqueTournament").get("slug"),
                    country_name=event.get("tournament")
                    .get("uniqueTournament")
                    .get("category")
                    .get("country")
                    .get("name"),
                    country_code=event.get("tournament")
                    .get("uniqueTournament")
                    .get("category")
                    .get("country")
                    .get("alpha2"),
                    has_performance_graph_feature=event.get("tournament")
                    .get("uniqueTournament")
                    .get("hasPerformanceGraphFeature")
                    or False,
                    has_event_player_statistics=event.get("tournament")
                    .get("uniqueTournament")
                    .get("hasEventPlayerStatistics")
                    or False,
                    scrapped_at=datetime.fromtimestamp(data.get("scrapped_at"), tz=timezone.utc),
                )

                season = sofascore.SofascoreSeasons(
                    id=event.get("season").get("id"),
                    name=event.get("season").get("name"),
                    tournament_id=event.get("tournament").get("uniqueTournament").get("id"),
                    year=event.get("season").get("year"),
                    scrapped_at=datetime.fromtimestamp(data.get("scrapped_at"), tz=timezone.utc),
                )

                match = sofascore.SofascoreMatches(
                    id=event.get("id"),
                    date=datetime.fromtimestamp(event.get("startTimestamp"), tz=timezone.utc),
                    tournament_id=event.get("tournament").get("id"),
                    season_id=event.get("season").get("id"),
                    round=event.get("roundInfo").get("round"),
                    status_id=event.get("status").get("code"),
                    home_team_id=event.get("homeTeam").get("id"),
                    away_team_id=event.get("awayTeam").get("id"),
                    home_score=event.get("homeScore").get("current"),
                    away_score=event.get("awayScore").get("current"),
                    has_players_statistics=event.get("hasEventPlayerStatistics") or False,
                    scrapped_at=datetime.fromtimestamp(data.get("scrapped_at"), tz=timezone.utc),
                )

                self.db.upsert_from_model(tournament)
                self.db.upsert_from_model(season)
                self.db.upsert_from_model(match)


def main():
    sofascore_matches = SofascoreMatches()
    sofascore_matches.run()


if __name__ == "__main__":
    main()
