## 小小爬虫项目
[![Build Status](https://travis-ci.org/liangliangyy/DjangoBlog.svg?branch=master)](https://travis-ci.org/liangliangyy/DjangoBlog) [![python3.7](https://img.shields.io/badge/python-3.7-brightgreen.svg)]()     
　　该项目当前可进行博客、拉钩、福彩数据的爬取，输出结果可存储为` json `、` xml `格式，也可以存储到` MySQL `数据库中。  

### 环境
* Python 3.7
* Scrapy 1.6.0
* MySQL 5.7.22

### 启动前的准备  
第一步：下载项目  
    
    git clone https://github.com/myminwang/spiders.git


第二步：安装依赖

    $cd spiders
    $pip install -r requirments.txt

第三步：配置数据库（非必须）
    
    1.设计数据表：
        方式一：参考/spiders/items.py中创建的Item，直接在数据库中创建数据表；
        方式二：终端执行$mysql -uroot -p spiders < articles.sql
        方式三：终端进入mysql，选择数据库后，执行>source articles.sql;
    2.配置数据库参数
    setting.py文件最后位置
    /spiders/pipelines.py中的MysqlPipeline(同步模式)、MysqlTwishtedPipeline(异步模式)
    

#### 一、博客文章爬取步骤  

1.查看main文件第13行及以后，仅保留第13行，注释14-15行  
2.查看setting.py中的ITEM_PIPELINES，根据需求选择保存的方式，其他方式需要注释，76行取消注释；
3.运行main.py文件，获取数据

#### 二、拉钩数据爬取步骤  

1.制作整合页面(需优化)  
`由于项目自身的问题，中间一些操作需要手动进行`  
(1)项目目录下，新建jobs.html文件，删除里面的默认内容 ，如果使用其他名字，需要修改/spiders/spiders/lagou.py文件中的23行  
(2)打开拉钩网站，职位搜索Python（或者其他），右击查看元素（F12）找到职位列表的代码，应该是在ul的标签内，折叠整个标签，右击复制元素  
(3)将元素粘贴到jobs.html，回车换行  
(4)拉钩网页点击下一页，再次复制ul标签，粘贴到jobs.html，拉钩应该有30个页面  
2.打开main.py文件，只执行execute('lagou')的，其他的execute注释掉，运行main文件会生成一个json文件  
3.使用pycharm打开json，格式化代码（必须），原始代码是一行的，必须格式化为多行  
4.注释lagou.py的23-27行，取消32-45行注释  
5.将新生成的json文件名，复制到32行里面  
9.运行运行main.py文件，会生成一个json文件 
10.重复第6步和第8、9步，直到所有的url被爬取  
11.如果当中某次爬取，全部是302错误，需要更换网络后，再按照第10步进行  
12.爬取数据完成后，会有生成的几个json文件，打开get_resualt.py文件，将每个文件名填入15行  
13.运行get_resualt.py文件，即可得到结果  


问题及优化方案：
1.未能抓取渲染后的页面，需要手工操作，可使用模拟浏览器内核的插件，如selenium、htmlunit、phantomjs等  
2.ip容易被屏蔽，需要更换一到两次网络，解决方法是添加ip地址池，在配置里修改，并添加中间件地址池处理类  


#### 三、爬取并分析双色球数据  

1.查看main.py文件，运行'shuangseqiu'的那一行，其他注释  
2.直接生成一个json文件，即为爬取的双色球中奖数据  
3.数据分析在predict_win_nums.py文件中，修改第10行文件名后，直接运行，在控制台看打印的结果  
4.使用思路一获得的结果，中头奖的概率约为1002万分之一，思路二约为670万分之一，当然机选的随机号码中奖概率约为135亿分之一  
5.另外，在知乎上有网友分享，国外已有华侨用超级计算机的统计算法分析过福体彩，得出的结论是：开奖结果是人为控制的，并非随机生成，当然感兴趣的同学可以用大数据和机器
学习进行分析，结果也是一样的  
6.说了这么多，就一句话：小赌怡情、大赌伤身、巨赌血本无归  
有时间、有精力，再有资金允许的情况下，就学学新知识，充充电，或者陪陪家人、四处逛逛