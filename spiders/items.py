# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime, re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "--myminwang"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y%m%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def remove_commet_tags(value):
    """去掉tags中提取的评论"""
    if '评论' in value:
        return ''
    else:
        return value


class ArticleItemLoader(ItemLoader):
    """重写ItemLoader"""
    default_output_processor = TakeFirst()


def get_nums(value):
    """获取数值"""
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def return_value(value):
    return value


class JobBoleArticaleItem(scrapy.Item):
    """指定item规则，只用Field()一个方式，里面可以进行函数计算，对传入的数据进行预处理"""
    title = scrapy.Field(
        # input_processor=MapCompose(lambda x: x + "--jobbole", add_jobbole)  # 将传递进来的值进行预处理
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),  # 对传入的数据预处理
        # output_processor=TakeFirst()    # 对传入的数据仅取第一个数值
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # 把url变成唯一的且长度固定的一个值
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_commet_tags),
        output_processor=Join(",")
    )


def replace_splash(value):
    return value.replace("/", "")


def handle_strip(value):
    return value.strip()


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


def job_desc_format(value):
    return re.sub(r'(<div\sclass=\"job-detail\">\n\s+<p>)|(<p>)|(</p>)|(</div>)|(<br>)', '', value)


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉勾网职位
    title = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(handle_strip, job_desc_format),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field(
        input_processor=MapCompose(handle_strip),
    )
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()


class ShuangseqiuItem(scrapy.Item):
    lottery_date = scrapy.Field()
    issue = scrapy.Field()
    winning_numbers = scrapy.Field()
    sales = scrapy.Field()
    first_prizes = scrapy.Field()
    second_prizes = scrapy.Field()
