import scrapy


class PressReleaseItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    publication_date = scrapy.Field()
    type = scrapy.Field()
    policy_areas = scrapy.Field()
    language = scrapy.Field()
