# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime, re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


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
