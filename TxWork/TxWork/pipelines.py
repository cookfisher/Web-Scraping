# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TxworkPipeline:
    def process_item(self, item, spider):
        mongo_client = pymongo.MongoClient()
        collection = mongo_client['py_spider']['tx_work_info']
        collection.insert_one(item)
        print('Inserted data: ', item.get('title'))
