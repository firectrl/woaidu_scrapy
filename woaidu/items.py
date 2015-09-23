# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DoubanbookItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()                  #书名
    author = scrapy.Field()                     #作者
    press = scrapy.Field()                      #出版社
    subtitle = scrapy.Field()                   #副标题
    original_name = scrapy.Field()              #原作名
    publishing_year = scrapy.Field()            #出版年
    page_cnt = scrapy.Field()                   #页数
    price = scrapy.Field()                      #定价
    binding = scrapy.Field()                    #装帧
    isbn = scrapy.Field()                       #ISBN
    evaluation = scrapy.Field()                 #豆瓣评价

class DoubanMoiveItem(scrapy.Item):
    name = scrapy.Field()#电影名
    year = scrapy.Field()#上映年份
    score = scrapy.Field()#豆瓣分数
    director = scrapy.Field()#导演
    classification = scrapy.Field()#分类
    actor = scrapy.Field()#演员
