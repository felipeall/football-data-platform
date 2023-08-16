import json
import re
from pathlib import Path

import scrapy
from scrapy import Request, Spider
from scrapy.http import TextResponse


class SofascoreGRE(Spider):
    name = "SofascoreGRE"
    allowed_domains = ["api.sofascore.com"]
    start_urls = [
        "https://api.sofascore.com/api/v1/team/5926/events/last/{page_id}",
        "https://api.sofascore.com/api/v1/team/5926/events/next/{page_id}",
    ]
    custom_settings = {
        "DEPTH_LIMIT": 0,
    }

    URL_REGEX = {
        "matches": r"team-(?P<id>\d+)-events",
        "matches_events": r"event-(?P<id>\d+)-lineups",
        "players": r"player-(?P<id>\d+)",
    }

    def start_requests(self):
        page_id = 0
        for url in self.start_urls:
            yield Request(
                url.format(page_id=page_id),
                meta={"start_url": url, "page_id": page_id},
                callback=self.parse_matches,
            )

    def parse_matches(self, response: TextResponse):
        self._save_response_to_json(response, category="matches")
        data = json.loads(response.body)

        for match_id in [d["id"] for d in data["events"]]:
            match_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
            yield scrapy.Request(match_url, callback=self.parse_matches_events)

        if data.get("hasNextPage"):
            next_page_id = 1 + response.meta.get("page_id")
            next_page_url = response.meta.get("start_url").format(page_id=next_page_id)
            yield Request(
                next_page_url,
                meta={"start_url": response.meta.get("start_url"), "page_id": next_page_id},
                callback=self.parse_matches,
            )

    def parse_matches_events(self, response: TextResponse):
        self._save_response_to_json(response, category="matches_events")
        data = json.loads(response.body)

        players_ids_home = [d["player"]["id"] for d in data["home"]["players"]]
        players_ids_away = [d["player"]["id"] for d in data["away"]["players"]]

        for player_id in players_ids_home + players_ids_away:
            player_url = f"https://api.sofascore.com/api/v1/player/{player_id}"
            yield scrapy.Request(player_url, callback=self.parse_players)

    def parse_players(self, response: TextResponse):
        self._save_response_to_json(response, category="players")

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
