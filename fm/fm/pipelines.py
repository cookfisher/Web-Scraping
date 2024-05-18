# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import pymongo
from itemadapter import ItemAdapter


class FmPipeline:
    def process_item(self, item, spider):
        download_path = os.getcwd() + '/download/'
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        type_ = item.get('type')
        if type_ == 'image':
            image_name = item.get('image_name')
            image_data = item.get('image_data')
            with open(download_path + image_name, 'wb') as f:
                f.write(image_data)
                print("Saved image: ", image_name)
        elif type_ == 'info':
            mongo_client = pymongo.MongoClient()
            collection = mongo_client['py_spider']['qingtingFM']
            collection.insert_one(item)
            print("Saved info: ", item.get('title'))
        else:
            print('Invalid data type...')







