'''
    2018年7月16日21:58:21

                爬取动态图片

    示例网站：http://qq.yh31.com
    示例链接：http://qq.yh31.com/zjbq/2920180.html
'''
'''
    实现步骤：
        1、导入第三方库
        2、获取目标网页
        3、解析目标网页
        4、下载目标网页数据
'''
# 1、导入第三方库
import requests,re

# 2、定义函数 获取目标网页
def get_urls():
    # 2.1、获取网页信息
    response = requests.get("http://qq.yh31.com/zjbq/2920180.html")
    
    # 3、解析目标网页
    # 3.1、找到图片地址 --> 正则匹配
    url_address = r'<img border="0".*? src="(.*?)"'
    # 3.2、筛选想要的数据 response.text:字符串;  response.content:二进制
    url_list = re.findall(url_address, response.text)

    return url_list

# 4、定义函数 下载目标网页数据 --> 动态图   
#       传入一个url的参数 这次的url是图片的目标地址而非网页的地址
#       传入一个name的参数 用来保存下载下来的图片的名称
def get_gif(url, pic_name):
    # 4.1、获取图片的url
    response = requests.get(url)

    # 4.2、保存图片     参数 wb ：二进制    a：追加
    with open(r'E:\001.File\03.Python_workspace\Python 3.0\03.Python_crawlers_Pro\08.getGIF\GetGif\%d.gif'%pic_name, 'wb') as ft:
        # 写入本地
        ft.write(response.content)


# 定义主函数入口
if __name__ == '__main__':
    # 返回的是一个列表
    url_list = get_urls()
            # 列表中的URL示例 ：                        /tp/Photo7/ZJBQ/20099/200909291701134159.gif
            # 我们能够访问的完成URL： http://qq.yh31.com/tp/Photo7/ZJBQ/20099/200909291701144684.gif
    # 循环提取列表中的信息 并且拼接完成URL
    # 定义一个默认的图片名称
    pic_name = 1
    for url in url_list:
        com_url = "http://qq.yh31.com" + url
        # 调用下载图片的函数 传入参数 --> 图片的地址
        get_gif(com_url, pic_name)
        # 自动生成一个图片名称 每次+1
        pic_name += 1
