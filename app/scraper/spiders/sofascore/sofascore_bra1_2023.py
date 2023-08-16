import json
import re
from pathlib import Path

from scrapy import Request, Spider
from scrapy.http import TextResponse


class SofascoreBRA12023(Spider):
    name = "SofascoreBRA12023"
    allowed_domains = ["api.sofascore.com"]
    start_urls = [
        "https://api.sofascore.com/api/v1/unique-tournament/325/season/48982/events/last/{page_id}",
        "https://api.sofascore.com/api/v1/unique-tournament/325/season/48982/events/next/{page_id}",
    ]
    custom_settings = {
        "DEPTH_LIMIT": 0,
    }

    URL_REGEX = {
        "teams": r"team-(?P<id>\d+)",
        "matches": r"unique-tournament-(?P<id>\d+)-season-(?P<season_id>\d+)-events",
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

        for team_id in [d["homeTeam"]["id"] for d in data["events"]]:
            team_url = f"https://api.sofascore.com/api/v1/team/{team_id}"
            yield Request(team_url, callback=self.parse_teams)

        for match_id in [d["id"] for d in data["events"]]:
            match_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
            yield Request(match_url, callback=self.parse_matches_events)

        if data.get("hasNextPage"):
            next_page_id = 1 + response.meta.get("page_id")
            next_page_url = response.meta.get("start_url").format(page_id=next_page_id)
            yield Request(
                next_page_url,
                meta={"start_url": response.meta.get("start_url"), "page_id": next_page_id},
                callback=self.parse_matches,
            )

    def parse_teams(self, response: TextResponse):
        self._save_response_to_json(response, category="teams")

    def parse_matches_events(self, response: TextResponse):
        self._save_response_to_json(response, category="matches_events")
        data = json.loads(response.body)

        players_ids_home = [d["player"]["id"] for d in data["home"]["players"]]
        players_ids_away = [d["player"]["id"] for d in data["away"]["players"]]

        for player_id in players_ids_home + players_ids_away:
            player_url = f"https://api.sofascore.com/api/v1/player/{player_id}"
            yield Request(player_url, callback=self.parse_players)

    def parse_players(self, response: TextResponse):
        self._save_response_to_json(response, category="players")

    def _save_response_to_json(self, response: TextResponse, category: str) -> None:
        assert category in self.URL_REGEX.keys()

        file_name = self._parse_file_name(response)
        regex_groups = re.search(self.URL_REGEX.get(category), file_name).groupdict()

        item = dict()
        item["id"] = regex_groups.get("id")
        if regex_groups.get("season_id"):
            item["season_id"] = regex_groups.get("season_id")
        item["url"] = response.url
        item["data"] = response.text

        file_path = Path(f"files/sofascore/{category}/{file_name}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(item))

    @staticmethod
    def _parse_file_name(response: TextResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])
