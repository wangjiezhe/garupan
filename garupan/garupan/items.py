# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GarupanItem(scrapy.Item):
    name = scrapy.Field()  # 角色名称
    description = scrapy.Field()  # 服饰名称
    image_urls = scrapy.Field()
    images = scrapy.Field()
