from datetime import datetime

import scrapy

from ec_press_scraper.items import PressReleaseItem


class PressReleasesSpider(scrapy.Spider):
    name = "press_releases"
    allowed_domains = ["ec.europa.eu"]

    base_api = (
        "https://ec.europa.eu/commission/presscorner/api/press-releases"
        "?page={page}&pageSize=20&language=en&type=press-release"
        "&sort=DESC&sortField=publicationDate"
    )

    def start_requests(self):
        # 60 stran × 20 záznamů = 1200 → z toho získáme posledních 1000
        for page in range(0, 60):
            yield scrapy.Request(
                self.base_api.format(page=page),
                callback=self.parse_list,
            )

    def parse_list(self, response):
        data = response.json()
        items = data.get("pressReleases") or data.get("items") or []

        for raw in items:
            pr_id = str(raw.get("id") or raw.get("reference") or raw.get("nid"))
            url = f"https://ec.europa.eu/commission/presscorner/detail/en/{pr_id}"

            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={"raw": raw, "url": url},
            )

    def parse_detail(self, response):
        raw = response.meta["raw"]
        url = response.meta["url"]

        # tělo zprávy – může být potřeba doladit podle skutečné struktury
        body_parts = response.css("#content *::text").getall()
        if not body_parts:
            body_parts = response.css("article *::text").getall()
        body = " ".join(p.strip() for p in body_parts if p.strip())

        date_str = (raw.get("publicationDate") or raw.get("date"))[:10]
        publication_date = datetime.fromisoformat(date_str).date()

        policy_areas_raw = raw.get("policyAreas") or raw.get("topics") or []
        policy_areas = [str(p) for p in policy_areas_raw]

        item = PressReleaseItem()
        item["id"] = str(raw.get("id") or raw.get("reference"))
        item["url"] = url
        item["title"] = raw.get("title") or raw.get("headline") or ""
        item["body"] = body
        item["publication_date"] = publication_date.isoformat()
        item["type"] = raw.get("type") or raw.get("contentType") or "Press release"
        item["policy_areas"] = policy_areas
        item["language"] = "en"
        yield item
