import json
from dataclasses import dataclass

from app.models import sofascore
from app.processing.base import BaseProcessing


@dataclass
class SofascoreMatches(BaseProcessing):
    files_path: str = "files/sofascore/matches/"

    def run(self):
        for data in self.files_data:
            events: list[dict] = json.loads(data["data"]).get("events")

            for event in events:
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
                    scrapped_at=self.parse_timestamp(data.get("scrapped_at")),
                )

                season = sofascore.SofascoreSeasons(
                    id=event.get("season").get("id"),
                    name=event.get("season").get("name"),
                    tournament_id=event.get("tournament").get("uniqueTournament").get("id"),
                    year=event.get("season").get("year"),
                    scrapped_at=self.parse_timestamp(data.get("scrapped_at")),
                )

                match = sofascore.SofascoreMatches(
                    id=event.get("id"),
                    date=self.parse_timestamp(event.get("startTimestamp")),
                    tournament_id=event.get("tournament").get("uniqueTournament").get("id"),
                    season_id=event.get("season").get("id"),
                    round=event.get("roundInfo", {}).get("round"),
                    status_id=event.get("status").get("code"),
                    home_team_id=event.get("homeTeam").get("id"),
                    away_team_id=event.get("awayTeam").get("id"),
                    home_score=event.get("homeScore").get("current"),
                    away_score=event.get("awayScore").get("current"),
                    has_players_statistics=event.get("hasEventPlayerStatistics") or False,
                    scrapped_at=self.parse_timestamp(data.get("scrapped_at")),
                )

                self.db.upsert_from_model(tournament)
                self.db.upsert_from_model(season)
                self.db.upsert_from_model(match)


def main():
    sofascore_matches = SofascoreMatches()
    sofascore_matches.run()


if __name__ == "__main__":
    main()
