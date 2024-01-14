import json
import re
from pathlib import Path

from scrapy.http import HtmlResponse, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TransfermarktGRE(CrawlSpider):
    name = "TransfermarktGRE"
    allowed_domains = ["transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/gremio-porto-alegre/startseite/verein/210"]

    DEPTH_LIMIT = 1
    URL_REGEX = {
        "clubs": r"verein-(?P<id>\d+)",
        "players": r"profil-spieler-(?P<id>\d+)",
        "market_value": r"-ceapi-marketValueDevelopment-graph-(?P<id>\d+)",
    }

    le_clubs = LinkExtractor(allow=r"gremio-porto-alegre/startseite/verein/\d+$")
    le_players = LinkExtractor(allow=r"/profil/spieler/\d+$", restrict_xpaths="//td[@class='hauptlink']")

    rules = (
        Rule(link_extractor=le_clubs, callback="process_clubs", follow=True),
        Rule(link_extractor=le_players, callback="process_players", follow=False),
    )

    def process_clubs(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="clubs")

    def process_players(self, response: HtmlResponse) -> None:
        self._save_response_to_json(response=response, category="players")

        # Market value
        player_id = response.url.split("/")[-1]
        url = "https://www.transfermarkt.com/ceapi/marketValueDevelopment/graph/{player_id}"
        yield Request(url=url.format(player_id=player_id), callback=self.process_market_value)

    def process_market_value(self, response: HtmlResponse):
        self._save_response_to_json(response=response, category="market_value")

    def _save_response_to_json(self, response: HtmlResponse, category: str) -> None:
        assert category in self.URL_REGEX.keys()

        file_name = self._parse_file_name(response)
        idx = re.search(self.URL_REGEX.get(category), file_name).groupdict().get("id")

        file_path = Path(f"files/tfmkt/{category}/{file_name}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps({"id": idx, "url": response.url, "data": response.text}))

    @staticmethod
    def _parse_file_name(response: HtmlResponse) -> str:
        page_name = response.url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])
