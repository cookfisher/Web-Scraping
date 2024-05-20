# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import pymongo
import os
from itemadapter import ItemAdapter


class DoubanPipeline:
    def process_item(self, item, spider):
        download_path = os.getcwd() + '/download/'
        if not os.path.exists(download_path):
            os.mkdir(download_path)

        type_ = item.get('type')
        if type_ == 'info':
            mongo_client = pymongo.MongoClient()
            collection = mongo_client['py_spider']['movie_info']
            collection.insert_one(item)
            print('Inserted data: ', item.get('title'))
        elif type_ == 'image':
            image_name = item.get('image_name')
            image_data = item.get('image_data')
            with open(download_path + image_name, 'wb') as f:
                f.write(image_data)
                print('Saved image: ', image_name)
        else:
            print('Invalid data type...')