# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class HcinfoPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    def open_spider(self, spider):
        if spider.name == 'HcInfoData':
            self.mongo_client = pymongo.MongoClient()
            self.collection = self.mongo_client['py_spider']['jc_info']

    def close_spider(self, spider):
        if spider.name == 'HcInfoData':
            self.mongo_client.close()

    def process_item(self, item, spider):
        if spider.name == 'HcInfoData':
            self.collection.insert_one(dict(item))
            print('Inserted into MongoDB:', item)
            return item