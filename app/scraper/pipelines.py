import re

import tldextract
from itemadapter import ItemAdapter
from scrapy import Item

from app.services.aws import AWS


class ParseItemPipeline:
    REGEX = {
        "transfermarkt": {
            "competitions": r"startseite-wettbewerb-(?P<id>\w+)-saison_id-(?P<season_id>\d+)",
            "clubs": r"startseite-verein-(?P<id>\d+)-saison_id-(?P<season_id>\d+)",
            "players": r"profil-spieler-(?P<id>\d+)",
            "market_value": r"-ceapi-marketValueDevelopment-graph-(?P<id>\d+)",
        },
    }

    def open_spider(self, spider):
        self.source = tldextract.extract(spider.allowed_domains[0]).domain
        self.url_regex = self.REGEX.get(self.source)

    def process_item(self, item: Item, spider):
        item["source"] = self.source
        item["file_name"] = self.__parse_file_name(url=item.get("url"))
        item["id"] = self.__extract_id(file_name=item["file_name"], path=item["path"])

        return item

    @staticmethod
    def __parse_file_name(url: str) -> str:
        page_name = url.split("://")[-1].replace("/", "-")
        return "".join([i if ord(i) < 128 else "-" for i in page_name])

    def __extract_id(self, file_name: str, path: str) -> str:
        return re.search(self.url_regex.get(path), file_name).groupdict().get("id")


class SaveItemPipeline:
    def open_spider(self, spider):
        self.aws = AWS()

    def process_item(self, item: Item, spider):
        self.aws.save_to_json(
            data=ItemAdapter(item).asdict(),
            path=f"files/{item['source']}/{item['path']}",
            file_name=item["file_name"],
        )

        return item
