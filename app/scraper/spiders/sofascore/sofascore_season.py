import json
import logging
from typing import Optional

from scrapy import Request, Spider
from scrapy.http import HtmlResponse

from app.scraper.items import ScrappedItem

log = logging.getLogger(__name__)


class SofascoreSeason(Spider):
    name = "sofascore_season"
    allowed_domains = ["api.sofascore.com"]
    start_urls = [
        "https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/events/last/{page_id}",
    ]
    custom_settings = {
        "DEPTH_LIMIT": 0,
    }

    TOURNAMENT_ID = ""
    SEASON_ID = ""

    def __init__(self, *args, **kwargs):
        super(SofascoreSeason, self).__init__(*args, **kwargs)
        if not self.TOURNAMENT_ID:
            log.error("TOURNAMENT_ID is required")
            raise ValueError("TOURNAMENT_ID is required")
        if not self.SEASON_ID:
            log.error("SEASON_ID is required")
            raise ValueError("SEASON_ID is required")

    def start_requests(self):
        page_id = 0
        for url in self.start_urls:
            url_formatted = url.replace("{tournament_id}", self.TOURNAMENT_ID).replace("{season_id}", self.SEASON_ID)
            yield Request(
                url_formatted.format(page_id=page_id),
                meta={"start_url": url_formatted, "page_id": page_id},
                callback=self._process_results,
                cb_kwargs={"path": "matches"},
            )

    def _process_results(self, response: HtmlResponse, path: str, metadata: Optional[dict] = None):
        yield ScrappedItem(
            url=response.url,
            data=response.text,
            path=path,
            metadata=metadata,
        )

        if path == "matches":
            data = json.loads(response.body)

            # Process Teams
            teams_ids_home = [d["homeTeam"]["id"] for d in data["events"]]
            teams_ids_away = [d["awayTeam"]["id"] for d in data["events"]]
            for team_id in set(teams_ids_home + teams_ids_away):
                team_url = f"https://api.sofascore.com/api/v1/team/{team_id}"
                yield Request(team_url, callback=self._process_results, cb_kwargs={"path": "teams"})

            # Process Matches
            for event in data["events"]:
                match_url = f"https://api.sofascore.com/api/v1/event/{event['id']}/lineups"
                yield Request(
                    match_url,
                    callback=self._process_results,
                    cb_kwargs={
                        "path": "matches_events",
                        "metadata": {"home_team_id": event["homeTeam"]["id"], "away_team_id": event["awayTeam"]["id"]},
                    },
                )

            # Process Next Page
            if data.get("hasNextPage"):
                next_page_id = 1 + response.meta.get("page_id")
                next_page_url = response.meta.get("start_url").format(page_id=next_page_id)
                yield Request(
                    next_page_url,
                    meta={"start_url": response.meta.get("start_url"), "page_id": next_page_id},
                    callback=self._process_results,
                    cb_kwargs={"path": "matches"},
                )

        if path == "matches_events":
            data = json.loads(response.body)

            players_ids_home = [d["player"]["id"] for d in data["home"]["players"]]
            players_ids_away = [d["player"]["id"] for d in data["away"]["players"]]

            for player_id in players_ids_home + players_ids_away:
                player_url = f"https://api.sofascore.com/api/v1/player/{player_id}"
                yield Request(player_url, callback=self._process_results, cb_kwargs={"path": "players"})
