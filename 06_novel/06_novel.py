'''
   Python 小说爬取  --以全书网为例
        url：http://www.quanshuwang.com/
        
        2018年5月13日20:29:44

    流程  -- 浏览器
        1、获取主页面源代码 -- 以《佣兵之王》为例      http://www.quanshuwang.com/book/0/742
        2、获取章节超链接
        3、获取章节超链接源码
        4、获取文本内容             
        5、保存到本地
'''

import urllib.request
import requests
import re

# 获取小说内容 这两种方法都可以获取到网页的源代码 但是两种方法导入的模块不一样
def getNovelContent_1():
    html = requests.get('http://www.quanshuwang.com/book/0/742')
    html.encoding = "GBK"       # 编码在网页源代码的head标签中查看
    # print(html.text)

def getNovelContent_2():
    html = urllib.request.urlopen("http://www.quanshuwang.com/book/0/742").read()
    html = html.decode("GBK")   
    # print(html)
    # 正则表达式匹配章节链接
    # <li><a href="http://www.quanshuwang.com/book/0/742/238294.html" title="第一章 初临异世，共4788字">第一章 初临异世</a></li>
    # compile 方法可以增加匹配效率
    urls = re.findall(re.compile(r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'), html)
    for url in urls:            # 获取到一个列表 第一个元素为 url 第二个元素为 章节名   即上面正则中带小括号的匹配结果
        # print(url)              # 循环输出列表
        novel_url = url[0]      # 获取章节url
        novel_title = url[1]    # 获取章节名称

        # 访问每一章节的url获取网页源码并转换编码
        chapter = urllib.request.urlopen(novel_url).read().decode("GBK")

        # 正则筛选获取文章内容
        reg = r'</script>&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<script type="text/javascript">'
        chapter_content = re.findall(re.compile(reg, re.S),chapter) # 列表形式
        # print(chapter_content[0])

        # 去除&nbsp;等  如下两种写法
        # resultText = chapter_content[0].replace("&nbsp;","").replace("<br />","")
        resultText = re.sub(r'&nbsp;|<br />', '', chapter_content[0])
        # print(resultText)

        # 保存到本地
        print("正在保存 %s"%novel_title)
        # f = open('06_{}.txt'.format(novel_title), 'w')
        # f.write(resultText)
        # f.close()

        # with open('06_{}.txt'.format(novel_title), 'w') as f:
        #     f.write(resultText)

        with open('06_小说.txt', mode='a+') as f:
            f.write('\n')
            f.write(resultText)

getNovelContent_2()


