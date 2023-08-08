import random
from pathlib import Path
from time import sleep

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FBRefGRE(CrawlSpider):
    name = "FBRefGRE"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/squads/d5ae3703/Gremio-Stats"]

    DEPTH_LIMIT = 1

    le_clubs = LinkExtractor(allow=r"/squads/\w+/Gremio-Stats$", restrict_xpaths="//td[@data-stat='team']")
    le_players = LinkExtractor(allow=r"/players/\w+/[\w-]+$", restrict_xpaths="//th[@data-stat='player']")
    le_matches = LinkExtractor(allow=r"/matches/\w+/[\w-]+$", restrict_xpaths="//td[@data-stat='match_report']")

    rules = (
        Rule(le_clubs, callback="process_club", follow=True),
        Rule(le_players, callback="process_player", follow=False),
        Rule(le_matches, callback="process_match", follow=False),
    )

    def process_club(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/fbref/clubs/{file_name}.html"
        Path(file_path).write_bytes(response.body)
        self._wait()

    def process_player(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/fbref/players/{file_name}.html"
        Path(file_path).write_bytes(response.body)
        self._wait()

    def process_match(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/fbref/matches/{file_name}.html"
        Path(file_path).write_bytes(response.body)
        self._wait()

    @staticmethod
    def _parse_file_name(response: HtmlResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])

    @staticmethod
    def _wait():
        sleep(random.uniform(2, 3))
