import scrapy


class GamedbsSpider(scrapy.Spider):
    name = "gamedbs"
    allowed_domains = ["garupan.gamedbs.jp"]
    start_urls = ["https://garupan.gamedbs.jp"]

    def parse(self, response):
        yield from response.follow_all(css=".dblst a", callback=self.parse_character)

    def parse_character(self, response):
        for img in response.css("ul.imgbox li a.hvr-grow"):
            yield {
                "title": img.attrib["title"],
                "img_url": img.attrib["href"]
            }
