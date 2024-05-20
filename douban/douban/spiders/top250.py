from typing import Iterable

import scrapy
from scrapy import cmdline, Request
from scrapy.http import HtmlResponse


class Top250Spider(scrapy.Spider):
    name = "top250"
    allowed_domains = ["douban.com", "doubanio.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def start_requests(self) -> Iterable[Request]:
        for page in range(10):
            url = f'https://movie.douban.com/top250?start={page * 25}&filter='
            print('Current page: ', url)
            yield scrapy.Request(url)

    def parse(self, response: HtmlResponse, **kwargs):
        # print(response.request.headers)
        li_list = response.xpath('//ol[@class="grid_view"]/li')
        for l in li_list:
            image_url = l.xpath('.//img/@src').extract_first()
            title = l.xpath('.//span[@class="title"][1]/text()').extract_first()
            rating_num = l.xpath(".//span[@class='rating_num']/text()").extract_first()
            people_num = l.xpath(".//div[@class='star']/span[4]/text()").extract_first()[:-3]

            print('--->', image_url, title, rating_num, people_num)

            yield {
                'type': 'info',
                'image': image_url,
                'title': title,
                'rating_num': rating_num,
                'people_num': people_num
            }

            yield scrapy.Request(url=image_url, callback=self.parse_image, cb_kwargs={'image_name': title})

    @staticmethod
    def parse_image(response, image_name):
        yield {
            'type': 'image',
            'image_name': image_name + '.jpg',
            'image_data': response.body
        }


if __name__ == '__main__':
    cmdline.execute("scrapy crawl top250 --nolog".split())