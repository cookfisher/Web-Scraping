import scrapy
from scrapy import cmdline
from scrapy.http import HtmlResponse


class QingtingSpider(scrapy.Spider):
    name = "qingting"
    allowed_domains = ["m.qingting.fm", "pic.qtfm.cn"]
    start_urls = ["https://m.qingting.fm/rank/"]

    def parse(self, response: HtmlResponse, **kwargs):
        a_list = response.xpath('//div[@class="rank-list"]/a')
        for l in a_list:
            rank_number = l.xpath('./div[@class="badge"]/text()').extract_first()
            img_url = l.xpath('./img/@src').extract_first()
            title = l.xpath('./div[@class="content"]/div[@class="title"]/text()').extract_first()
            desc = l.xpath('./div[@class="content"]/div[@class="desc"]/text()').extract_first()
            play_number = l.xpath('.//div[@class="info-item"][1]/span/text()').extract_first()

            yield {
                'type': 'info',
                'rank_number': rank_number,
                'img_url': img_url,
                'title': title,
                'desc': desc,
                'play_number': play_number
            }

            yield scrapy.Request(img_url, callback=self.parse_image, cb_kwargs={'image_name': title})

    def parse_image(self, response, image_name):
        yield {
            'type': 'image',
            'image_name': image_name + ".png",
            'image_data': response.body
        }


if __name__ == '__main__':
    cmdline.execute('scrapy crawl qingting --nolog'.split())