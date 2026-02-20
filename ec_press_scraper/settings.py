BOT_NAME = "ec_press_scraper"

SPIDER_MODULES = ["ec_press_scraper.spiders"]
NEWSPIDER_MODULE = "ec_press_scraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "ec_press_scraper.pipelines.JsonlWriterPipeline": 300,
}

USER_AGENT = "ec-press-scraper (+https://example.com)"
