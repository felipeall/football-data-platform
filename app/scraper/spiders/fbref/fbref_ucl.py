import random
from time import sleep

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.scraper.items import ScrappedItem


class FBrefUCL(CrawlSpider):
    name = "FBrefUCL"
    allowed_domains = ["fbref.com"]
    start_urls = ["https://fbref.com/en/comps/8/Champions-League-Stats"]
    custom_settings = {
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "CONCURRENT_REQUESTS": 1,
    }

    le_teams = LinkExtractor(
        allow=r"/squads/\w+/[\w\-]+$",
        restrict_xpaths="//table[./caption[contains(text(), 'League Table Table')]]//td[@data-stat='team']",
    )
    le_matches = LinkExtractor(allow=r"/matches/\w+/[\w-]+$", restrict_xpaths="//td[@data-stat='match_report']")
    le_players = LinkExtractor(allow=r"/players/\w+/[\w-]+$", restrict_xpaths="//th[@data-stat='player']")
    le_scouting_reports = LinkExtractor(
        allow=r"/players/\w+/scout/\w+/[\w-]+-Scouting-Report$",
        restrict_xpaths="//div[@id='all_scout_summary']",
    )

    rules = (
        Rule(le_teams, follow=True, callback="_process_results", cb_kwargs={"path": "teams"}),
        # Rule(le_matches, follow=False, callback="_process_results", cb_kwargs={"path": "matches"}),
        Rule(le_players, follow=True, callback="_process_results", cb_kwargs={"path": "players"}),
        Rule(
            le_scouting_reports,
            follow=False,
            callback="_process_results",
            cb_kwargs={"path": "scouting_reports"},
        ),
    )

    def _process_results(self, response: HtmlResponse, path: str):
        self._wait()
        yield ScrappedItem(
            url=response.url,
            data=response.text,
            path=path,
        )

    @staticmethod
    def _wait():
        sleep(random.uniform(2, 3))
