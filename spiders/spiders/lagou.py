# -*- coding: utf-8 -*-
import re
from time import sleep

import scrapy
from urllib import parse
from scrapy.http import Request
from spiders.items import LagouJobItem, LagouJobItemLoader


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/5677575.html']

    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    header = {
        'HOST': 'www.lagou.com',
        'Referer': 'https://www.lagou.com',
        'User-Agent': agent
    }

    job_urls = open('job_urls.html', 'r').read()
    p = re.compile(r'data-positionid="(\d+)"?')
    python_urls = p.findall(job_urls)
    python_urls = ['https://www.lagou.com/jobs/' + url + '.html' for url in python_urls]

    def parse(self, response):
        """"""
        for python_url in self.python_urls:
            yield Request(url=python_url,callback=self.job_detail,meta={
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



