import logging

from scrapy.http import HtmlResponse, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.scraper.items import ScrappedItem

log = logging.getLogger(__name__)


class Transfermarkt(CrawlSpider):
    name = "transfermarkt"
    allowed_domains = ["transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/-/startseite/wettbewerb/{tournament_id}/plus/?saison_id={season_id}"]

    le_competitions = LinkExtractor(
        allow=r"/startseite/wettbewerb/\w+/plus/\?saison_id=\d+$",
        restrict_xpaths="//a[@class='tm-tab tm-tab__active--parent']",
    )
    le_clubs = LinkExtractor(
        allow=r"/startseite/verein/\d+/saison_id/\d+$",
        restrict_xpaths="//table[@class='items']//td[@class='hauptlink no-border-links']",
    )
    le_players = LinkExtractor(
        allow=r"/profil/spieler/\d+$",
        restrict_xpaths="//div[@id='yw1']//td[@class='hauptlink']",
    )

    rules = (
        Rule(
            link_extractor=le_competitions,
            follow=True,
            callback="_process_results",
            cb_kwargs={"path": "competitions"},
        ),
        Rule(link_extractor=le_clubs, follow=True, callback="_process_results", cb_kwargs={"path": "clubs"}),
        Rule(link_extractor=le_players, follow=False, callback="_process_results", cb_kwargs={"path": "players"}),
    )

    TOURNAMENT_ID = ""
    SEASON_ID = ""

    def __init__(self, *args, **kwargs):
        super(Transfermarkt, self).__init__(*args, **kwargs)
        if not self.TOURNAMENT_ID:
            log.error("TOURNAMENT_ID is required")
            raise ValueError("TOURNAMENT_ID is required")
        if not self.SEASON_ID:
            log.error("SEASON_ID is required")
            raise ValueError("SEASON_ID is required")

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url.format(tournament_id=self.TOURNAMENT_ID, season_id=self.SEASON_ID),
                cb_kwargs={"path": "competitions"},
            )

    def _process_results(self, response: HtmlResponse, path: str):
        yield ScrappedItem(
            url=response.url,
            data=response.text,
            path=path,
        )

        if path == "players":
            player_id = response.url.split("/")[-1]
            url = "https://www.transfermarkt.com/ceapi/marketValueDevelopment/graph/{player_id}"
            yield Request(
                url=url.format(player_id=player_id),
                callback=self._process_results,
                cb_kwargs={"path": "market_value"},
            )
