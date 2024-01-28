import scrapy


class TfmktItem(scrapy.Item):
    url = scrapy.Field()
    data = scrapy.Field()
    path = scrapy.Field()
    source = scrapy.Field()
    file_name = scrapy.Field()
    id = scrapy.Field()
