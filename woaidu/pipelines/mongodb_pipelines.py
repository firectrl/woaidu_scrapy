# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class MongoDBPipeline(object):

    MONGODB_BOOK_COLLECTION = 'douban_book'
    MONGODB_MOVIE_COLLECTION = 'douban_movie'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            mongo_uri=settings.get('MONGODB_URI'),
            mongo_db=settings.get('MONGODB_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #Remove invalid data
        valid = True
        for data in item:
          if not data:
            valid = False
        if not valid:
            return item

        if spider.name == 'douban_book':
            collection = self.db[self.MONGODB_BOOK_COLLECTION]
            collection.insert(dict(item))
        elif spider.name == 'douban_movie':
            collection = self.db[self.MONGODB_MOIVE_COLLECTION]
            new_movie=[{
                "name":item['name'][0],
                "year":item['year'][0],
                "score":item['score'][0],
                "director":item['director'],
                "classification":item['classification'],
                "actor":item['actor']
            }]
            collection.insert(new_movie)
        return item