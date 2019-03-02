'''
    Python 爬取中科院院士信息   
        url：http://www.cae.cn/cae/html/main/col48/column_48_1.html
        
        2018年5月13日12:14:07
'''
# 导入模块
import re
import time
import requests

# 过程式编程
url = 'http://www.cae.cn/cae/html/main/col48/column_48_1.html'

# 请求数据
html = requests.get(url)    # 网页源码
html.encoding = 'UTF-8'     # 指定编码
print(html.status_code)     # 状态码
# print(html.text)            # 文本信息
# print(html.url)             # 请求网址
# print(html.content)         # 字节流
# print(html.headers)         # 头信息
# print(html.cookies)         # cookies值

# 提取文本信息 --院士名单中人名所在链接 格式：/cae/html/main/colys/数字.html" target="_blank
number = re.findall('/cae/html/main/colys/(\d+).html" target="_blank', html.text)   # 返回的是列表
# print(number)

# for n in number:
for n in number[:10]:    # 获取前 10 个number
    # nextUrl = 'http://www.cae.cn/cae/html/main/colys/' + n + '.html'
    nextUrl = 'http://www.cae.cn/cae/html/main/colys/{}.html'.format(n)
    # print(nextUrl)
    # 再次发送请求
    html_2 = requests.get(nextUrl)
    html_2.encoding = 'UTF-8'
    # print(html_2.text)
    # 提取文本信息 --院士的个人信息介绍  格式：<div class="intro"><p> 文本信息 </p></div>
    text_2 = re.findall('<div class="intro">(.*?)</div>', html_2.text, re.S)  # .*?不能匹配换行,加上参数re.S匹配换行
    # print(text_2)   # 结果中存在一部分&nbsp;<p>之类的转义字符
    resultText = re.sub(r'&ensp;|<p>|&nbsp;|</p>', '', text_2[0]).strip()      # 去掉转义字符与空格
    # print(resultText)

    # 写入文件
    # 这种写法不需要关闭文件。
    # mode = 'a+'   追加的方式写入
    with open(r'E:\001.File\03.Python_workspace\Python 3.0\03.Python_crawlers_Pro\04_中国工程院信息爬取.txt', mode = 'a+') as f:
        f.write(resultText + '\n' * 2)
    
print("写入完成")