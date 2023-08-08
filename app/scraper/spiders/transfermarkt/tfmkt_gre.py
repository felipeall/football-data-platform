import random
from pathlib import Path
from time import sleep

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TransfermarktGRE(CrawlSpider):
    name = "TransfermarktGRE"
    allowed_domains = ["transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/gremio-porto-alegre/startseite/verein/210"]

    DEPTH_LIMIT = 1

    le_clubs = LinkExtractor(allow=r"gremio-porto-alegre/startseite/verein/\d+$")
    le_players = LinkExtractor(allow=r"/profil/spieler/\d+$", restrict_xpaths="//td[@class='hauptlink']")
    le_market_value = LinkExtractor(
        allow=r"/marktwertverlauf/spieler/\d+$", restrict_xpaths="//a[@class='content-link']",
    )

    rules = (
        Rule(link_extractor=le_clubs, callback="process_club", follow=True),
        Rule(link_extractor=le_players, callback="process_player", follow=True),
        Rule(link_extractor=le_market_value, callback="process_market_value", follow=True),
    )

    def process_club(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/tfmkt/clubs/{file_name}.html"
        Path(file_path).write_bytes(response.body)

    def process_player(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/tfmkt/players/{file_name}.html"
        Path(file_path).write_bytes(response.body)

    def process_market_value(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/tfmkt/market_value/{file_name}.html"
        Path(file_path).write_bytes(response.body)

    @staticmethod
    def _parse_file_name(response: HtmlResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])

    @staticmethod
    def _wait():
        sleep(random.uniform(2, 3))
