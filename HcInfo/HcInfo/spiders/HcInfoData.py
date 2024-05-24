import scrapy
from scrapy import Request, cmdline
from HcInfo.items import HcInfoItem

class HcinfodataSpider(scrapy.Spider):
    name = "HcInfoData"
    allowed_domains = ["www.cninfo.com.cn"]
    # start_urls = ["http://www.cninfo.com.cn/new/disclosure"]

    def start_requests(self):
        url = 'http://www.cninfo.com.cn/new/disclosure'

        for page in range(1, 16):
            data = {
                "column": "szse_latest",
                "pageNum": str(page),
                "pageSize": "30",
                "sortName": "",
                "sortType": "",
                "clusterFlag": "true"
            }

            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse, dont_filter=False)


    def parse(self, response, **kwargs):
        for info_list in response.json()['classifiedAnnouncements']:
            for info in info_list:
                item = HcInfoItem()
                item['announcementTitle'] = info['announcementTitle']
                item['announcementTypeName'] = info['announcementTypeName']
                item['batchNum'] = info['batchNum']
                item['secName'] = info['secName']
                item['adjunctType'] = info['adjunctType']
                yield item

if __name__ == '__main__':
    cmdline.execute('scrapy crawl HcInfoData'.split())

