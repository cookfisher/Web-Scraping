# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import json
import pymongo
import redis
from scrapy.exceptions import DropItem


class TxworkCheckPipeline:
    def open_spider(self, spider):
        if spider.name == 'tx_work_info':
            self.redis_client = redis.Redis()

    def process_item(self, item, spider):
        if spider.name == 'tx_work_info':
            item_str = json.dumps(item)
            md5_hash = hashlib.md5()
            md5_hash.update(item_str.encode('utf-8'))
            hash_value = md5_hash.hexdigest()

            if self.redis_client.get(f'tx_work_item_filter:{hash_value}'):
                raise DropItem("Duplicate item...")
            else:
                self.redis_client.set(f'tx_work_item_filter:{hash_value}', item_str)
            return item

    def close_spider(self, spider):
        if spider.name == 'tx_work_info':
            self.redis_client.close()


class TxworkMongoPipeline:
    def open_spider(self, spider):
        if spider.name == 'tx_work_info':
            self.mongo_client = pymongo.MongoClient()
            self.collection = self.mongo_client['py_spider']['tx_work_info']
    def process_item(self, item, spider):
        if spider.name == 'tx_work_info':
            self.collection.insert_one(item)
            print('Inserted data: ', item.get('title'))
            return item

    def close_spider(self, spider):
        if spider.name == 'tx_work_info':
            self.mongo_client.close()


class TxworkFilePipeline:
    def open_spider(self, spider):
        if spider.name == 'tx_work_info':
            self.file = open('tx_work_info.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if spider.name == 'tx_work_info':
            self.file.write(json.dumps(item, ensure_ascii=False, indent=4) + ',\n')
            return item

    def close_spider(self, spider):
        if spider.name == 'tx_work_info':
            self.file.close()

