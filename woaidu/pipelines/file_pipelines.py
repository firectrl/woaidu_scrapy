# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.book_file = None
        self.movie_file = None

    def open_spider(self, spider):
        if spider.name == 'douban_book':
            self.book_file = codecs.open('douban_book.json', 'w', encoding='utf-8')
        elif spider.name == 'douban_movie':
            self.movie_file = codecs.open('douban_movie.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        if spider.name == 'douban_book':
            self.book_file.close()
        elif spider.name == 'douban_movie':
            self.movie_file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        if spider.name == 'douban_book':
            self.book_file.write(line)
        elif spider.name == 'douban_movie':
            self.movie_file.write(line)

        return item