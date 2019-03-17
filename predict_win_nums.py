#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "问道编程"
__date__ = "2019/03/15 11:52"

import json
from collections import Counter
from functools import reduce


all_datas = open('2019-03-17 08:53:43.573400.json', 'r').read()
all_datas = json.loads(all_datas)  # list
win_nums = list()
for data_ in all_datas:
    win_nums.append(data_['winning_numbers'])


# 中奖规则：
def win_foo(chose_num):
    """选中的号码，历史中奖纪录"""
    history_wins = {'一等奖：': 0, '二等奖：': 0, '三等奖：': 0, '四等奖：': 0, '五等奖：': 0, '六等奖：': 0}

    blue_get = 0
    red_get = 0

    chose_blue = chose_num.pop()
    for win_num in win_nums:
        win_blue = win_num[-1]
        if chose_blue == win_blue:
            blue_get = 1
        red_get = len([chose_n for chose_n in chose_num if chose_n in win_num[:-1]])

        if red_get == 6 and blue_get == 1:
            history_wins['一等奖：'] += 1
        elif red_get == 6:
            history_wins['二等奖：'] += 1
        elif red_get == 5 and blue_get == 1:
            history_wins['三等奖：'] += 1
        elif red_get == 5 or (red_get == 4 and blue_get == 1):
            history_wins['四等奖：'] += 1
        elif red_get == 4 or (red_get == 3 and blue_get == 1):
            history_wins['五等奖：'] += 1
        elif blue_get == 1:
            history_wins['六等奖：'] += 1

    return history_wins


# 预测开奖号码
# 思路一：每个球出现概率前三的数字
print('思路一：每个球出现概率前十的数字')
res_01 = list()
for i in range(7):
    print('------------------------------------------')
    print('第' + str(i + 1) + '个球，出现概率前十的数字\n按平均概率计算：红球每个数出现概率为 3.03%,篮球每个数字出现的概率为 6.25%\n')
    win_list = [win_num[i] for win_num in win_nums]

    res = Counter(win_list).most_common(10)  # list  [(),(),()]
    print('排名  数字  出现次数  出现概率%')
    for j in range(10):
        print(' %d    %s    %s      %.2f' % (j + 1, res[j][0], res[j][1], int(res[j][1]) / 23.88))
        if j == 0:
            res_01.append(res[j][0])
    print('------------------------------------------')

# 思路二：红球出现概率最大的前六个数字，篮球出现概率前三的数字
print('------------------------------------------')
print('------------------------------------------')
res_02 = list()

all_red_win = reduce(lambda x, y: x + y, [win_num[:6] for win_num in win_nums])
all_blue_win = reduce(lambda x, y: x + y, [win_num[6].split() for win_num in win_nums])
length_red = len(all_red_win)
length_blue = len(all_blue_win)
res_red = Counter(all_red_win).most_common(10)  # list  [(),(),()]
res_blue = Counter(all_blue_win).most_common(10)  # list  [(),(),()]
print('思路二：概率最大的前十个数字')
print('红球')
print('排名  数字  出现次数  出现概率%')
for j in range(10):
    print(' %d    %s    %s      %.2f' % (j + 1, res_red[j][0], res_red[j][1], int(res_red[j][1]) / (length_red / 100)))
    if j < 6:
        res_02.append(res_red[j][0])

print('------------------------------------------')
print('篮球')
print('排名  数字  出现次数  出现概率%')
for j in range(10):
    print(' %d    %s    %s      %.2f' % (
        j + 1, res_blue[j][0], res_blue[j][1], int(res_blue[j][1]) / (length_blue / 100)))
    if j == 0:
        res_02.append(res_blue[j][0])

print('++++++++++++++++++++++++++++++++++')
print('当前预测下一期中奖的号码为：')
print('思路一：', res_01)
history_wins = win_foo(res_01)
print('历史中奖情况：', history_wins)
print('思路二：', res_02)
history_wins = win_foo(res_02)
print('历史中奖情况：', history_wins)
