# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HcInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    announcementTitle = scrapy.Field()
    announcementTypeName = scrapy.Field()
    batchNum = scrapy.Field()
    secName = scrapy.Field()
    adjunctType = scrapy.Field()

