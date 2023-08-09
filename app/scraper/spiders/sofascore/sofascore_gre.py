import json
import re
from pathlib import Path

import scrapy
from scrapy.http import TextResponse


class SofascoreGRE(scrapy.Spider):
    name = "SofascoreGRE"
    allowed_domains = ["api.sofascore.com"]
    start_urls = ["https://api.sofascore.com/api/v1/team/5926/events/last/0"]

    URL_REGEX = {
        "clubs": r"team-(?P<id>\d+)-events",
        "matches": r"event-(?P<id>\d+)-lineups",
        "players": r"player-(?P<id>\d+)",
    }

    def parse(self, response: TextResponse):
        self._save_response_to_json(response, category="clubs")
        data = json.loads(response.body)

        for match_id in [d["id"] for d in data["events"]]:
            match_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
            yield scrapy.Request(match_url, callback=self.parse_match)

    def parse_match(self, response: TextResponse):
        self._save_response_to_json(response, category="matches")
        data = json.loads(response.body)

        players_ids_home = [d["player"]["id"] for d in data["home"]["players"]]
        players_ids_away = [d["player"]["id"] for d in data["away"]["players"]]

        for player_id in players_ids_home + players_ids_away:
            player_url = f"https://api.sofascore.com/api/v1/player/{player_id}"
            yield scrapy.Request(player_url, callback=self.parse_player)

    def parse_player(self, response: TextResponse):
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
