from scrapy.http import HtmlResponse, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.scraper.items import ScrappedItem


class TransfermarktBRA1(CrawlSpider):
    name = "TransfermarktBRA1"
    allowed_domains = ["transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1"]
    URL_MARKET_VALUE = "https://www.transfermarkt.com/ceapi/marketValueDevelopment/graph/{player_id}"

    le_competitions = LinkExtractor(
        allow=r"/startseite/wettbewerb/\w+/saison_id/\d+$",
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
