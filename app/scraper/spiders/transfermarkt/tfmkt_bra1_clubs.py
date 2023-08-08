from pathlib import Path

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TfmktBRA1(CrawlSpider):
    name = "TfmktBRA1"
    allowed_domains = ["transfermarkt.com"]
    start_urls = [
        "https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1",
    ]
    DEPTH_LIMIT = 1

    le_clubs = LinkExtractor(allow=r"/startseite/verein/\d+$")
    le_players = LinkExtractor(allow=r"/profil/spieler/\d+$", restrict_xpaths="//th[@data-stat='player']")

    rules = (
        Rule(le_clubs, callback="process_club", follow=True),
        Rule(le_players, callback="process_player", follow=False),
    )

    def parse_player_profile(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/tfmkt/players/profile/{file_name}.html"
        Path(file_path).write_bytes(response.body)

    def parse_club_profile(self, response: HtmlResponse) -> None:
        file_name = self._parse_file_name(response)
        file_path = f"files/tfmkt/clubs/profile/{file_name}.html"
        Path(file_path).write_bytes(response.body)

    @staticmethod
    def _parse_file_name(response: HtmlResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])
