import scrapy
from scrapy import cmdline
from scrapy.http import HtmlResponse


class QingtingSpider(scrapy.Spider):
    name = "qingting"
    allowed_domains = ["m.qingting.fm"]
    start_urls = ["https://m.qingting.fm/rank/"]

    def parse(self, response: HtmlResponse, **kwargs):
        print(response.text)


if __name__ == '__main__':
    cmdline.execute('scrapy crawl qingting'.split())
