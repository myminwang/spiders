# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs, os
import json
import pymysql
import pymysql.cursors
import datetime

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter, XmlItemExporter
from twisted.enterprise import adbapi  # 提供异步化数据库处理的方式


class SpidersPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """自己写的：将结果输出到json文件中，需要在配置中添加该管道及优先级"""

    def __init__(self):
        file_name = str(datetime.datetime.now().date()) + '.json'
        self.file = codecs.open('other.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spinder_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    """使用scrapy提供的JSON EXPORT 导出json文件"""

    def __init__(self):
        file_name = str(datetime.datetime.now()) + '.json'
        self.file = open(file_name, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class XmlExportPipeline(object):
    """使用scrapy提供的xml EXPORT 导出xml文件"""
    def __init__(self):
        file_name = str(datetime.datetime.now().date()) + '.xml'
        self.file = open(file_name, 'wb')
        self.exporter = XmlItemExporter(file=self.file)
        self.exporter.start_exporting()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()



class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='******', database='spiders')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into articles(title,create_date,url,url_object_id,front_image_url,front_image_path,praise_nums,comment_nums,fav_nums,content,tags) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            self.cursor.execute(insert_sql, (
                item['title'], item['create_date'], item['url'], item['url_object_id'], item['front_image_url'],
                item['front_image_path'], item['praise_nums'], item['fav_nums'], item['comment_nums'], item['content'],
                item['tags']))
            self.conn.commit()
            # execute和commit操作是同步操作，先后执行，但是爬虫爬取并解析数据的速度，大于数据库录入的数据，后期数据量大时，会形成堵塞

        except Exception as e:
            print(e)
            self.conn.rollback()

    def close_spider(self, spider):
        self.conn.close()


class MysqlTwishtedPipeline(object):
    """爬取的数据解析，同数据库数据存储，进行异步化操作"""
    def __init__(self, dbpool):
        """引入连接池"""
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """初始化连接池参数"""
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
        )
        dbpool = adbapi.ConnectionPool('pymysql',**dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        """连接池操作"""
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        """处理异步插入的异常"""
        print(failure)

    def do_insert(self,cursor,item):
        """执行具体插入操作"""
        insert_sql = """
            insert into articles(title,create_date,url,url_object_id,front_image_url,front_image_path,praise_nums,comment_nums,fav_nums,content,tags) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql, (
            item['title'], item['create_date'], item['url'], item['url_object_id'], item['front_image_url'][0],
            item['front_image_path'], item['praise_nums'], item['fav_nums'], item['comment_nums'], item['content'],
            item['tags']))
        # 执行语句后，自动进行commit操作


class ArticlaImagePipeline(ImagesPipeline):
    """获取下载图片的本地路径"""

    def item_completed(self, results, item, info):
        if 'front_image_path' in item:
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path  # 获取的是相对路径
        return item
