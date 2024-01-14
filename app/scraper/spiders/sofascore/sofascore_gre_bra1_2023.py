import json
import re
from pathlib import Path

import scrapy
from scrapy import Request, Spider
from scrapy.http import TextResponse


class SofascoreGREBRA12023(Spider):
    name = "SofascoreGREBRA12023"
    allowed_domains = ["api.sofascore.com"]
    start_urls = [
        "https://api.sofascore.com/api/v1/team/5926/events/last/{page_id}",
    ]
    custom_settings = {
        "DEPTH_LIMIT": 0,
    }

    URL_REGEX = {
        "team_events": r"team-(?P<id>\d+)-events",
        "event": r"event-(?P<id>\d+)$",
        "event_lineups": r"event-(?P<id>\d+)-lineups",
        "player": r"player-(?P<id>\d+)$",
    }

    TOURNAMENT_ID = 83
    TEAM_ID = 5926

    def start_requests(self):
        page_id = 0
        for url in self.start_urls:
            yield Request(
                url.format(page_id=page_id),
                meta={"start_url": url, "page_id": page_id},
                callback=self.parse_team_events,
            )

    def parse_team_events(self, response: TextResponse):
        self._save_response_to_json(response, category="team_events")
        data = json.loads(response.body)

        for event_id in [d["id"] for d in data["events"] if d["tournament"]["id"] == self.TOURNAMENT_ID]:
            event_url = f"https://api.sofascore.com/api/v1/event/{event_id}"
            yield scrapy.Request(event_url, callback=self.parse_event)

        if data.get("hasNextPage") and any(
            "tournament" in item and item["tournament"]["id"] == self.TOURNAMENT_ID for item in data.get("events", [])
        ):
            next_page_id = 1 + response.meta.get("page_id")
            next_page_url = response.meta.get("start_url").format(page_id=next_page_id)
            yield Request(
                next_page_url,
                meta={"start_url": response.meta.get("start_url"), "page_id": next_page_id},
                callback=self.parse_team_events,
            )

    def parse_event(self, response: TextResponse):
        self._save_response_to_json(response, category="event")
        data = json.loads(response.body)
        event_id = data["event"]["id"]
        event_lineups_url = f"https://api.sofascore.com/api/v1/event/{event_id}/lineups"

        if data["event"]["homeTeam"]["id"] == self.TEAM_ID:
            team_side = "home"
        elif data["event"]["awayTeam"]["id"] == self.TEAM_ID:
            team_side = "away"
        else:
            team_side = None

        if team_side:
            yield Request(event_lineups_url, callback=self.parse_event_lineups, meta={"team_side": team_side})

    def parse_event_lineups(self, response: TextResponse):
        self._save_response_to_json(response, category="event_lineups")
        data = json.loads(response.body)

        players_ids = [d["player"]["id"] for d in data[response.meta.get("team_side")]["players"]]
        for player_id in players_ids:
            player_url = f"https://api.sofascore.com/api/v1/player/{player_id}"
            yield scrapy.Request(player_url, callback=self.parse_player)

    def parse_player(self, response: TextResponse):
        self._save_response_to_json(response, category="player")

    def _save_response_to_json(self, response: TextResponse, category: str):
        assert category in self.URL_REGEX.keys()

        file_name = self._parse_file_name(response)
        idx = re.search(self.URL_REGEX.get(category), file_name).groupdict().get("id")

        file_path = Path(f"files/sofascore/{category}/{file_name}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps({"id": idx, "url": response.url, "data": response.json()}))

    @staticmethod
    def _parse_file_name(response: TextResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])
