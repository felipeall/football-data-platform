import json
import random
import re
from pathlib import Path
from time import sleep

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TransfermarktBRA1(CrawlSpider):
    name = "TransfermarktBRA1"
    allowed_domains = ["transfermarkt.com"]
    start_urls = [
        "https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1",
    ]

    DEPTH_LIMIT = 1
    URL_REGEX = {
        "clubs": r"verein-(?P<id>\d+)",
        "players": r"profil-spieler-(?P<id>\d+)",
        "market_values": r"marktwertverlauf-spieler-(?P<id>\d+)",
    }

    le_clubs = LinkExtractor(allow=r"/startseite/verein/\d+$")
    le_players = LinkExtractor(allow=r"/profil/spieler/\d+$", restrict_xpaths="//td[@class='hauptlink']")
    le_market_values = LinkExtractor(
        allow=r"/marktwertverlauf/spieler/\d+$",
        restrict_xpaths="//a[@class='content-link']",
    )

    rules = (
        Rule(link_extractor=le_clubs, callback="process_clubs", follow=True),
        Rule(link_extractor=le_players, callback="process_players", follow=True),
        Rule(link_extractor=le_market_values, callback="process_market_values", follow=True),
    )

    def process_clubs(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="clubs")

    def process_players(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="players")

    def process_market_values(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="market_values")

    def _save_response_to_json(self, response: HtmlResponse, category: str) -> None:
        assert category in self.URL_REGEX.keys()

        file_name = self._parse_file_name(response)
        idx = re.search(self.URL_REGEX.get(category), file_name).groupdict().get("id")

        file_path = Path(f"files/tfmkt/{category}/{file_name}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps({"id": idx, "url": response.url, "data": response.text}))

        self._wait()

    @staticmethod
    def _parse_file_name(response: HtmlResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])

    @staticmethod
    def _wait() -> None:
        sleep(random.uniform(2, 3))
