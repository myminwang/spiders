# -*- coding: utf-8 -*-
import scrapy

from spiders.items import ShuangseqiuItem
from scrapy.http import Request


class ShuangseqiuSpider(scrapy.Spider):
    name = 'shuangseqiu'
    allowed_domains = ['kaijiang.zhcw.com']
    start_urls = ['http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html']

    def parse(self, response):
        """url处理"""
        all_pages = response.xpath('//*[@class="pg"]/strong/text()').extract()[0]
        all_pages = int(all_pages)

        for i in range(1, all_pages + 1):
            yield Request(url='http://kaijiang.zhcw.com/zhcw/html/ssq/list_' + str(i) + '.html',
                          callback=self.winning_detail)

    def winning_detail(self, response):
        """数据解析"""
        item = ShuangseqiuItem()
        for i in range(3, 23):
            item['lottery_date'] = response.xpath('//table/tr[' + str(i) + ']/td[1]/text()').extract()[0]
            item['issue'] = response.xpath('//table/tr[' + str(i) + ']/td[2]/text()').extract()[0]
            item['winning_numbers'] = response.xpath('//table/tr[' + str(i) + ']/td[3]/em/text()').extract()
            item['sales'] = response.xpath('//table/tr[' + str(i) + ']/td[4]/strong/text()').extract()[0]
            item['first_prizes'] = response.xpath('//table/tr[' + str(i) + ']/td[5]/strong/text()').extract()[0]
            item['second_prizes'] = response.xpath('//table/tr[' + str(i) + ']/td[6]/strong/text()').extract()[0]

            yield item
