import json

import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MongoDBPipeline:

    def __init__(self, server, port, database, collection):
        self.server = server
        self.port = port
        self.database = database
        self.collection = collection
        self.DB = {
            "caa_search": "caa_search",
            "caa_site_detail": "caa_site_detail",
            "mlit_parent": "mlit_parent",
            "mlit_child": "mlit_child"
        }
        self.FILES = {
            "caa_search": "caa_search",
            "caa_site_detail": "caa_site_detail",
            "mlit_parent": "mlit_parent",
            "mlit_child": "mlit_child"
        }
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            server=crawler.settings.get('MONGODB_SERVER'),
            port=crawler.settings.get('MONGODB_PORT'),
            database=crawler.settings.get('MONGODB_DB'),
            collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        # mongo db client to save items
        self.client = pymongo.MongoClient(self.server, self.port)
        self.db = self.client[self.database]

        # open file to write items
        for key, value in self.FILES.items():
            self.files.update({key: open(f'{value}.jsonl', 'w')})

    def close_spider(self, spider):
        self.client.close()

        # open file to write items
        for key, value in self.FILES.items():
            self.files[key].close()

    def process_item(self, item, spider):
        if item.get("to_db", False) and item.get("type") in self.DB:
            self.DB[item.get("type")].insert_one(dict(item))
        if item.get("to_file", False) and item.get("type") in self.files:
            line = json.dumps(item, ensure_ascii=False) + "\n"
            self.files[item.get("type")].write(line)
        return item
