#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "问道编程"
__date__ = "2019/03/11 12:42"

import hashlib


def get_md5(url):
    if isinstance(url, str):   # python3 默认是unincode编码的，而hash不接收这类编码，需要判断url后转换为utf-8编码
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5('http://python.jobbole.com/89337/'.encode('utf-8')))