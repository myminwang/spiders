#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "问道编程"
__date__ = "2019/03/12 15:48"

import os, json, xlwt, datetime

# wbk = xlwt.Workbook()
# sheet = wbk.add_sheet('sheet 1')
# sheet.write(0,1,'test text')#第0行第一列写入内容
# wbk.save('test.xls')

print(os.listdir())

files = ['2019-03-12 17:43:25.761526.json',]

wbk = xlwt.Workbook()
sheet = wbk.add_sheet(str(datetime.datetime.now()))

titles = ['职位名称', '职位链接', '薪资', '工作城市', '工作经验', '学历要求', '职位类型', '发布时间', '职位诱惑', '职位描述', '工作地点', '公司介绍']
for i in range(len(titles)):
    sheet.write(0, i, titles[i])

rows = 1
for file in files:
    job_res = []
    file_data = open(file)
    job_res = json.load(file_data)
    file_data.close()
    for job_re in job_res:
        title = job_re.get('title', '')
        url = job_re.get('url', '')
        salary = job_re.get('salary', '')
        job_city = job_re.get('job_city', '')
        work_years = job_re.get('work_years', '')
        degree_need = job_re.get('degree_need', '')
        job_type = job_re.get('job_type', '')
        publish_time = job_re.get('publish_time', '')
        job_advantage = job_re.get('job_advantage', '')
        job_desc = job_re.get('job_desc', '')
        job_addr = job_re.get('job_addr', '')
        company_url = job_re.get('company_url', '')

        sheet.write(rows, 0, title)
        sheet.write(rows, 1, url)
        sheet.write(rows, 2, salary)
        sheet.write(rows, 3, job_city)
        sheet.write(rows, 4, work_years)
        sheet.write(rows, 5, degree_need)
        sheet.write(rows, 6, job_type)
        sheet.write(rows, 7, publish_time)
        sheet.write(rows, 8, job_advantage)
        sheet.write(rows, 9, job_desc)
        sheet.write(rows, 10, job_addr)
        sheet.write(rows, 11, company_url)
        rows += 1

file_name = str(datetime.datetime.now()) + '.xls'
wbk.save(file_name)
