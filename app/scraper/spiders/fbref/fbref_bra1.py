import json
import random
import re
from pathlib import Path
from time import sleep

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FBRefBRA1(CrawlSpider):
    name = "FBRefBRA1"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/comps/24/Serie-A-Stats"]
    custom_settings = {
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "CONCURRENT_REQUESTS": 1,
    }

    URL_REGEX = {
        "clubs": r"squads-(?P<id>\w+)-",
        "matches": r"matches-(?P<id>\w+)-",
        "players": r"players-(?P<id>\w+)-",
    }

    le_clubs = LinkExtractor(allow=r"/squads/\w+/[\w\-]+$", restrict_xpaths="//td[@data-stat='team']")
    le_matches = LinkExtractor(allow=r"/matches/\w+/[\w-]+$", restrict_xpaths="//td[@data-stat='match_report']")
    le_players = LinkExtractor(allow=r"/players/\w+/[\w-]+$", restrict_xpaths="//th[@data-stat='player']")

    rules = (
        Rule(le_clubs, callback="parse_clubs", follow=True),
        Rule(le_matches, callback="parse_matches", follow=False),
        Rule(le_players, callback="parse_players", follow=False),
    )

    def parse_clubs(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="clubs")

    def parse_matches(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="matches")

    def parse_players(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="players")

    def _save_response_to_json(self, response: HtmlResponse, category: str):
        assert category in self.URL_REGEX.keys()

        file_name = self._parse_file_name(response)
        idx = re.search(self.URL_REGEX.get(category), file_name).groupdict().get("id")

        file_path = Path(f"files/fbref/{category}/{file_name}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps({"id": idx, "url": response.url, "data": response.text}))

        self._wait()

    @staticmethod
    def _parse_file_name(response: HtmlResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])

    @staticmethod
    def _wait():
        sleep(random.uniform(2, 3))
