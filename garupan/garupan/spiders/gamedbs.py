import scrapy
from garupan.items import GarupanItem


class GamedbsSpider(scrapy.Spider):
    name = "gamedbs"
    allowed_domains = ["garupan.gamedbs.jp"]
    start_urls = ["https://garupan.gamedbs.jp"]

    def parse(self, response):
        yield from response.follow_all(css=".dblst a", callback=self.parse_character)

    def parse_character(self, response):
        name = response.css("title::text").re(r"(.+) \|.+")[0]
        for img in response.css("ul.imgbox li a.hvr-grow"):
            item = GarupanItem()
            item["name"] = name
            item["description"] = img.attrib["title"]
            item["image_urls"] = [img.attrib["href"]]
            yield item
