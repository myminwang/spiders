#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "问道编程"
__date__ = "2019/03/12 12:28"

import json, re, datetime, os
import codecs
import requests

# datas_file = open('2019-03-12 14:57:02.949376.json', 'r').read()
# # datas_file = open('111.json', 'r').read()
#
# datas_file = re.sub(r',\n\s+{\n\s+"url": "https://www.lagou.com/jobs/\d{5,7}.html"\n\s+}', '', datas_file)
#
# with open('112.json', 'w') as fa:
#     fa.write(datas_file)
#
# file_name = '2019-03-12 15:08:58.494065.json'
# job_has = open(file_name, 'r').read()
#
# re_bad_urls = re.compile(r',\n\s+{\n\s+"url": "(https://www.lagou.com/jobs/\d{5,7}.html)"\n\s+}')
#
# bad_urls = re_bad_urls.findall(job_has)
# print(bad_urls)
#
# print('尚未爬取的数据有 ', len(bad_urls), ' 条，马上为主人爬取.....')
# if bad_urls:
#     with open(file_name, 'w+') as fa:
#         fa.write(re.sub(re_bad_urls, '', job_has))
# else:
#     print('已完成所有数据爬取')

# file = codecs.open('2.json', 'a', encoding='utf-8')
#
#
# item = {"title": "xxxxxxx","url": "xxxxx","salary": "fffffff "}
# item_ = file+list(dict(item))
# lines = json.dumps(item_) + '\n'
# file.write(lines)
#
# item = {"title": "qqqq","url": "wwww","salary": "eeee "}
# lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
# file.write(lines)
#
# file.close()

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
headers = {
    'HOST': 'www.lagou.com',
    'Referer': 'https://www.lagou.com',
    'User-Agent': agent
}

res = requests.get('https://www.lagou.com/jobs/5189420.html', headers=headers)
print(res.text)
