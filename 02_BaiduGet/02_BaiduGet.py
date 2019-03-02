# 模拟Baidu搜索发送Get请求， 返回网页数据
#       2018年4月30日20:48:27

# step 1 --导包
import requests
import re

# step 9 ################################ 代码重构 - 动态获取搜索参数 - 定义参数 ################################
key = '程序设计'

# step 2 --百度搜索  "程序设计"  然后复制 url  url编码：%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1
# url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=monline_3_dg&wd=%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1&oq=%25E7%25A8%258B%25E5%25BA%258F%25E8%25AE%25BE%25E8%25AE%25A1&rsv_pq=eb75570f000f79e7&rsv_t=78e2HO6SCkFgV7w8Sh0FOw8t1cVb0yZICeeDhIeCpN8DzIvmYNW5nHtWUOZx%2FxhliPv8&rqlang=cn&rsv_enter=0'

# step 9 ################################ 代码重构 - 动态获取搜索参数 - 重构url ################################
url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=monline_3_dg&oq=%25E7%25A8%258B%25E5%25BA%258F%25E8%25AE%25BE%25E8%25AE%25A1&rsv_pq=eb75570f000f79e7&rsv_t=78e2HO6SCkFgV7w8Sh0FOw8t1cVb0yZICeeDhIeCpN8DzIvmYNW5nHtWUOZx%2FxhliPv8&rqlang=cn&rsv_enter=0'

# step 3 --伪装请求头  字典格式  --> 第一个文件 触发远为document的请求头
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0' }

# step 9 ################################ 代码重构 - 动态获取搜索参数 - 参数字典 ################################
# 请求参数
# data = {
#     'wd':key
# }
# step 10 重构 -- 翻页参数
'''
    不同页的URL中会发现一个参数pn  第一页pn = 0  第二页pn = 10 第三页 pn = 20 ……
    为实现翻页爬取，将下面所有的发送请求的代码放置在for循环中。

    为了防止频繁的打开关闭，且有可能造成覆盖风险，所以将文件的打开关闭放在for循环之外
'''
fb = open('%s.txt' % key, 'w')
for i in range(3):
    data = {
        'wd':key,
        'pn':i * 10
    }

    # step 4 --发送HTTP请求
    # response = requests.get(url, headers = headers)

    # step 9 ################################ 代码重构 - 动态获取搜索参数 - 提交参数 ################################
    # step 9 ############################ 代码重构 - 增加两个参数 -搜索参数 请求超时参数 #############################
    response = requests.get(url, headers = headers, params = data, timeout = 10)

    # step 5 --获取响应数据 -- 网页源码
    html = response.text

    # 打印获取到的响应数据
    # print(html)

    # step 6 --正则表达式获取div  匹配 html 中所有以 <div class="result c-container " 开头的部分 中 http:www.baidu.com/link?url= 开头的
    urls = re.findall(r'<div class="result c-container ".*?"(http://www.baidu.com/link\?url=.*?)".*?', html, re.S)  # re.s 匹配不可见字符。由于.*?匹配中可能出现回车换行等不可见字符
    # print(urls[0])   # 匹配的结果是一个列表 输出第一条  这里的URL其实只是百度指向的一条跳转链接，并非真实的URL

    # step 8 -- 数据持久化 写入本地文本文件
    # fb = open('02_程序设计.txt', 'w')

    # step 9 ################################ 代码重构 - 动态写入文件名 - 占位符 ################################
    # fb = open('%s.txt' % key, 'w')

    # step 7 -- 循环所有的URL 并携带伪装的请求头访问 获取重定向的URL
    for b_url in urls:
        # print(b_url)
        res = requests.get(b_url, headers = headers)
        # print(res.url)      # 获取到重定向后的URL

    # step 8 -- 数据持久化 写入本地文本文件
        fb.write(res.url)
        fb.write('\n')
    # fb.close()
fb.close()

print('Finished')
############################# 附加知识 ################################
'''
网络爬虫：
    模拟浏览器自动去互联网上下载一些需要的网络资源

网络资源：
    我们在互联网上能够访问的到的图片、文件等

URL：
    全球统一资源定位符

开发爬虫的步骤：
    1. 找到目标资源
        -- 目标数据所在的页面
        -- 目标数据对应的URL
    2. 数据的加载
        -- 分析数据发送HTTP请求的方式
    3. 模拟发送HTTP请求
    4. 提取数据
        -- 数据清洗
    5. 数据持久化
        -- 入库
        -- 写入本地文件

'''