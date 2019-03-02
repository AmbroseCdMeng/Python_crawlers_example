'''
    2018年8月12日11:09:19
    Python爬取短视频

    目标网站：  www.pearvideo.com

        HTTP协议    端口号 80
        HTTPS协议   端口号 443

    任意一个示例视频的src属性   src="http://video.pearvideo.com/mp4/adshort/20180811/cont-1409661-12647534_adpkg-ad_hd.mp4"
'''
'''
    requests 库的七个主要方法
        requests.request()      构造一个请求，支持一下的各种方法
        requests.get()          获取HTML的主要方法
        requests.head()         获取HTML头部信息的主要方法
        requests.post()         向HTML网页提交Post请求的方法
        requests.put()          向HTML网页提交Put请求的方法
        requests.patch()        向HTML提交局部修改的请求
        requests.delete()       向HTML提交删除请求       
'''

'''
基本思路：
    获取目标网站首页
        www.pearvideo.com
    获取目标分类地址（以体育分类为例）
        http://www.pearvideo.com/category_9
    获取所有目标短视频的URL地址
        http://www.pearvideo.com/video_1409661
        http://www.pearvideo.com/video_1409999
        ...
    获取所有目标短视频的SRC原地址
        http://video.pearvideo.com/mp4/adshort/20180811/cont-1409661-12647534_adpkg-ad_hd.mp4
    下载视频
'''
import requests
from urllib.request import urlretrieve  # 用于下载功能
import re
import os
import time

# 使用xpath筛选页面元素  效果与之前使用正则一样
from lxml import etree

# 下载
def download(url):

    # 伪造请求头
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    # 获取页面源码(携带请求头)
    # url = "http://www.pearvideo.com/category_9"
    html = requests.get(url, headers = header)
    # print(html) # 200 响应成功
    # print(html.text)

    # 把文本文件处理成可解析的对象
    html = etree.HTML(html.text)
    # print(html) # XPATH 对象

    # 获取短视频的ID
    '''
    <div class="vervideo-bd">
        <a href="video_1410037" class="vervideo-lilink actplay" target="_blank">
            <div class="vervideo-img">
                <div class="verimg-view"><div class="img" style="background-image: url(http://image.pearvideo.com/cont/20180812/cont-1410037-11467557.jpg);">
                </div>
            </div>
            <div class="cm-duration">00:55</div>
            </div>
            <div class="vervideo-title">皮克宣布退出国家队,要专注于巴萨</div>
        </a>
        <div class="actcont-auto">
            <a href="author_11549117" class="column">看球</a>
            <span class="fav" data-id="1410037">65</span>
        </div>
    </div>
    '''
    # 以下语句意为：获取所有class属性为vervideo-bd的div标签   下的a标签的href属性
    # @符号代表获取属性     []  匹配属性    /  下面的标签
    video_id = html.xpath("//div[@class='vervideo-bd']/a/@href")

    # 同下面正则  用正则就不能吧HTML.text 转换成对象了
    # reg = r'<a href="(.*?)" class="vervideo-lilink actplay"'
    # video_id = re.findall(reg, requests.get("http://www.pearvideo.com/category_9").text)

    print(video_id)

    # 拼接URL地址
    video_url = []
    starturl = r'http://www.pearvideo.com'
    for vid in video_id:
        print(id)
        newurl = starturl + r'/' + vid
        # print(newurl)
        video_url.append(newurl)
    print(video_url)

    # 获取所有目标短视频的SRC原地址 (重点)
    # 发现video标签的src属性 在HTML页面源文件中不存在！！！ 也就是说无法直接从Html.text中获取到video的src属性
    # <video webkit-playsinline="" playsinline="" x-webkit-airplay="" autoplay="autoplay" src="http://video.pearvideo.com/mp4/adshort/20180812/cont-1410037-12650358_adpkg-ad_hd.mp4" style="width: 100%; height: 100%;"></video>
    
    # 我们走一个捷径，直接复制video的src地址，搜索一下html页面源码中是否存在
    # 发现，虽然不存在video标签，但是视频的src地址在JS中动态加载之后保存在了JS代码中。我们可以通过正则来提取
    # <script type="text/javascript"> var contId="1410037",liveStatusUrl="liveStatus.jsp",liveSta="",playSta="1",autoPlay=!1,isLiving=!1,isVrVideo=!1,hdflvUrl="",sdflvUrl="",hdUrl="",sdUrl="",ldUrl="",
    # srcUrl="http://video.pearvideo.com/mp4/adshort/20180812/cont-1410037-12650358_adpkg-ad_hd.mp4",vdoUrl=srcUrl,skinRes="//www.pearvideo.com/domain/skin",videoCDN="//video.pearvideo.com";
    
    # 如此获取视频真实的播放地址  req = r'srcUrl="(.*?)"'     但是我们需要获取所有
    for purl in video_url:
        # 获取每个播放页面的源代码(携带请求头)
        videoHtml = requests.get(purl, header).text
        reg = r'srcUrl="(.*?)"'
        playurl = re.findall(reg, videoHtml)
        # print(playurl)

        # 获取视频的标题
        reg = r'<h1 class="video-tt">(.*?)</h1>'
        video_title = re.findall(reg, videoHtml)
        # print(video_title[0])   # 直接获取的到的List数据类型  使用[0]只获取标题字符串

        # 下载保存
        print("正在下载视频:%s"%video_title[0])
        # 指定下载路径  -- 导入OS模块  自动创建目录  os.listdir()  当前目录下所有文件
        path = "videos"
        if path not in os.listdir():
            os.mkdir(path)
        
        urlretrieve(playurl[0], path+"/%s.mp4"%video_title[0])

        # 到这里 已经可以下载视频了 但是只能下载当前页面的 12 个视频
        # 扩展一下 如何动态的加载更多视频 即相当于在页面上点击 “加载更多” 选项？
        # 发现 滚动到页面底端时 会自动触发一个URL  测试三次 对比触发的URL的不同
        # http://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=9&start=24&mrd=0.8532441084852755&hotContIds=1409661,1409867,1409890
        # http://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=9&start=36&mrd=0.34623290995601486&hotContIds=1409661,1409867,1409890
        # http://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=9&start=48&mrd=0.8934378948320691&hotContIds=1409661,1409867,1409890

        # 发现，除了后面的mrd之外，之后一个地方不同且有规律。就是start=...  每加载一次，增加 12 。mrd的值经测试实际上不影响访问的结果
        # 但是要注意 CategoryID 的值，应该是与选择的视频类型有关的，所以暂时写的加载更多的方法只适用于我们测试的类型
# 加载更多的方法
def downloadmore(category_id):
    n = 12  # 第一次加载更多时 start 应该等于 12
    while True:
        if n > 48:
            return
        url = "http://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=%d&start=%d"%(category_id, n)
        n+=12
        # print(url)
        time.sleep(1)   # 反爬的一种。有些网站的反爬机制会限定持续性的下载，所以每下载一个视频时休息一下
        download(url)

# 获取多种分类的视频
category = [9, 10]
for category_id in category:
    downloadmore(category_id)

