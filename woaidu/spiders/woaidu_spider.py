# -*- coding: utf-8 -*-

import logging
import scrapy
import urllib

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from urlparse import urljoin
from scrapy.http import Request
from doubanbook.items import DoubanbookItem


class DoubanBookSpider(scrapy.Spider):
    name = 'douban_book'
    allowed_domains = ['douban.com']
    start_urls = ['http://book.douban.com/tag/?icn=index-nav']


    def parse(self, response):
        #category_urls = response.xpath('//*[@id="content"]/div/div[1]/div[2]/div/table/tbody/tr/td/a/@href').extract()
        category_urls = response.xpath('//*[@id="content"]/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[1]/a/text()').extract()
        for url in category_urls:
            #yield Request(url=url, callback=self.parse_category)

            new_url = 'http://www.douban.com/tag/{category}/book'\
                .format(category=urllib.quote(url.encode(response.encoding)))
            yield Request(url=new_url, callback=self.parse_category_all)

    def parse_category(self, response):
        # subject_urls = response.xpath('//*[@id="book"]/dl/dd/a/@href').extract()
        # #subject_urls = response.xpath('//*[@id="book"]/dl[7]/dd/a/@href').extract()
        # for url in subject_urls:
        #     yield Request(url=url, callback=self.parse_item)

        category_all_urls =\
            response.xpath('//*[@id="content"]/div/div[1]/div/ul/li/div[1]/h2/a/@herf').extract()
        for url in category_all_urls:
            yield Request(url=url, callback=self.parse_category_all)

    def parse_category_all(self, response):
        category_all_urls =\
            response.css('#content > div > div.article > div.paginator > span.next > a::attr(href)').extract()
        for url in category_all_urls:
            new_url = urljoin(response.url, url)
            yield Request(url=new_url, callback=self.parse_category_all)

        subject_urls = response.xpath('//*[@id="content"]/div/div[1]/div[1]/dl/dd/a/@href').extract()
        for url in subject_urls:
            yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        item = DoubanbookItem()
        book_name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract()
        item['book_name'] = "/".join(book_name)
        author = response.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        item['author'] = "/".join(author)

        book_new_infos = []
        book_infos = response.xpath('//*[@id="info"]/text()').extract()
        for info in book_infos:
            info = info.strip()
            if info:
                book_new_infos.append(info)

        if len(book_new_infos) == 8:
            item['press'] = book_new_infos[0]
            item['subtitle'] = book_new_infos[1]
            item['original_name'] = book_new_infos[2]
            item['publishing_year'] = book_new_infos[3]
            item['page_cnt'] = book_new_infos[4]
            item['price'] = book_new_infos[5]
            item['binding'] = book_new_infos[6]
            item['isbn'] = book_new_infos[7]
        elif len(book_new_infos) == 7:
            item['press'] = book_new_infos[0]
            item['subtitle'] = ''
            item['original_name'] = book_new_infos[1]
            item['publishing_year'] = book_new_infos[2]
            item['page_cnt'] = book_new_infos[3]
            item['price'] = book_new_infos[4]
            item['binding'] = book_new_infos[5]
            item['isbn'] = book_new_infos[6]
        elif len(book_new_infos) == 6:
            item['press'] = book_new_infos[0]
            item['subtitle'] = ''
            item['original_name'] = ''
            item['publishing_year'] = book_new_infos[1]
            item['page_cnt'] = book_new_infos[2]
            item['price'] = book_new_infos[3]
            item['binding'] = book_new_infos[4]
            item['isbn'] = book_new_infos[5]
        elif len(book_new_infos) == 5:
            item['press'] = book_new_infos[0]
            item['subtitle'] = ''
            item['original_name'] = ''
            item['publishing_year'] = book_new_infos[1]
            item['page_cnt'] = book_new_infos[2]
            item['price'] = book_new_infos[3]
            item['binding'] = ''
            item['isbn'] = book_new_infos[4]
        elif len(book_new_infos) == 3:
            item['press'] = book_new_infos[0]
            item['subtitle'] = ''
            item['original_name'] = ''
            item['publishing_year'] = book_new_infos[1]
            item['page_cnt'] = ''
            item['price'] = ''
            item['binding'] = ''
            item['isbn'] = book_new_infos[2]

        evaluation = response.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
        if len(evaluation) == 0:
            item['evaluation'] = ''
        else:
            item['evaluation'] = evaluation[0].strip()

        return item