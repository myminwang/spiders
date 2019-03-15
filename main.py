#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "问道编程"
__date__ = "2019/03/11 10:39"

import os, sys

from scrapy.cmdline import execute

# 设置项目根目录(获取当前文件所在文件夹的绝对路径)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(['scrapy', 'crawl', 'jobbole'])  # 相当于subprocess.call  类似于os.system
# execute(['scrapy', 'crawl', 'lagou'])
execute(['scrapy', 'crawl', 'shuangseqiu'])
