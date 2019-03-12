# -*- coding: utf-8 -*-
import re, os, datetime
from time import sleep

import scrapy
from urllib import parse
from scrapy.http import Request
from spiders.items import LagouJobItem, LagouJobItemLoader


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/4164766.html']

    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    header = {
        'HOST': 'www.lagou.com',
        'Referer': 'https://www.lagou.com',
        'User-Agent': agent
    }

    job_urls = open('jobs.html', 'r').read()
    p = re.compile(r'data-positionid="(\d+)"?')
    python_urls = p.findall(job_urls)
    python_urls = list(set(python_urls))
    python_urls = ['https://www.lagou.com/jobs/' + url + '.html' for url in python_urls]


    def parse(self, response):
        """"""
        # file_name = '2019-03-12 17:43:25.761526.json'
        # job_has = open(file_name, 'r').read()
        # re_bad_urls = re.compile(r',\n\s+{\n\s+"url": "(https://www.lagou.com/jobs/\d{5,7}.html)"\n\s+}')
        # bad_urls = re_bad_urls.findall(job_has)
        # print('尚未爬取的数据有 ', len(bad_urls), ' 条，马上为主人爬取.....')
        # sleep(3)
        #
        # if bad_urls:
        #     self.python_urls = bad_urls
        #     with open(file_name, 'w+') as fa:
        #         fa.write(re.sub(re_bad_urls, '', job_has))
        # else:
        #     print('已完成所有数据爬取')
        #     self.close()

        for python_url in self.python_urls:
            yield Request(url=python_url, callback=self.job_detail, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302]
            }, headers=self.header)

    def job_detail(self, response):
        """页面解析"""
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name span::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("salary", ".salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")

        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("company_name", "#job_company dt a div h2::text")

        job_item = item_loader.load_item()

        return job_item
