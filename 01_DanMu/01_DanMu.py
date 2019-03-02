'''
    Bilibili网站直播间弹幕抓取与发送弹幕 -- 案例
                                        2018年4月30日12:40:34

        各大网站由于反爬机制不同，抓取难度与方法也不同，本例以Bilibili为例。

        关于开发者工具抓包，推荐使用火狐浏览器或谷歌浏览器自带的开发者工具(F12)
'''
####################### 获取弹幕 ###########################
####################### 前期准备 ###########################

# 1. 登录Bilibili并进入直播间，打开开发者工具，"网络"选项卡，刷新页面或点击重新载入按钮，自动抓取页面数据
'''
    状态：     200--正常     404--页面丢失
    方法：     Post--提交    Get--获取
                Post  -- 必须提交参数才可以访问
                Get   -- 不需要提交任何参数直接可以访问
'''
# 2. 找到弹幕对应的文件      --在Firefox浏览器中，文件名msg的文件对应的"响应"选项卡中存放的就是弹幕信息、发送人ID、昵称、时间戳等
#                          --在Google浏览器中，文件名msg的文件对应的"Preview"选项卡存放的是弹幕信息

####################### 发送弹幕 ###########################
####################### 前期准备 ###########################

''' 
获取发送信息
    # 清空监视器，发送一条弹幕，然后暂停监视器，此时，监视器中抓取到的名为Send的post请求信息就为刚才发送的信息。
    # 参数如下：
        color	16777215                                -- 字体颜色
        csrf_token	e1577bd2347f0ca58c3055764a1a52a3    -- 跨域攻击
        fontsize	25                                  -- 字体大小
        mode	1
        msg	666                                         -- 所发送的文本
        rnd	1525084816                                  -- 时间戳
        roomid	3604605                                 -- 房间号
    # 消息头：
        请求网址  https://api.live.bilibili.com/msg/send
        请求方法  POST
'''

####################### 登录账号 ###########################
####################### 前期准备 ###########################
'''
    账号密码信息存储在浏览器的cookie值中
        首先还是定义在发送弹幕前期准备中抓取到的Send信息中
            Firefox 浏览器中  右侧直接有 cookie 选项卡，但不建议在这里寻找。 建议在"消息头"选项卡 -> 请求头  -> cookie ：
'''

####################### 案例开始 ###########################

# step 1 -- 导包
import time
import random
import requests # pysinstaller --打包成exe可执行文件

# step 2 -- 下载弹幕文件
'''msg的详细信息界面简介 
        参数:
            csrf_token:     	                    -- 该参数用于防止跨域攻击
            data_behavior_id:                       -- 监控用户行为id信息
            data_source_id:                         -- 资源信息
            roomid:17778                            -- 直播房间的id信息
            visit_id:a5roej4ic8hs                   -- 游客访问的id信息
        消息头：
            请求网址  https://api.live.bilibili.com/ajax/msg
            请求方法  POST
            远程地址
            请求头/响应头信息
'''

# step 3 -- 定义发送弹幕的类
class DanMuSend:

    # step 4 -- 定义初始化方法
    def __init__(self, roomid):

        # step 5 -- 定义获取弹幕方法的全局变量与参数
        self.roomid = str(roomid)
            #  -- 定义全局变量存储url    self.变量名 -- 定义全局变量     ★ 此处url为Post请求地址 在"消息头"中，而非直播间地址
        self.urlGet = 'https://api.live.bilibili.com/ajax/msg'
            #  -- 定义全局变量存储需要提交的参数，并获取弹幕     参数须以字典的格式存储
        self.formGet = {   'roomid':self.roomid,
                        'visit_id':'6zb84c0sd0cg'   }
        

    # step 6 -- 定义获取弹幕方法
    def getDanMu(self):
        # -- 提交数据   data  是关键字参数
        self.htmlGet = requests.post(self.urlGet, data = self.formGet)
        print(self.htmlGet)    # 打印提交状态  200 --正常   404 -- 失败
        # print(self.htmlGet.json())     # 获取弹幕信息的Json文件
        # print(self.htmlGet.json()['data']['room'][0]['text'])      # 返回一条弹幕  -- data -> room -> 0 -> text 是"响应"中json文件对应的的标签
        self.danmu = list(map(lambda x : self.htmlGet.json()['data']['room'][x]['text'], range(10)))   # 使用补充知识中的map函数与Lambda表达式返回最近的10条弹幕
        self.message = self.danmu[random.randint(7, 9)];   # 列表的切片操作。随机选取后三条弹幕中的一条存储起来准备发送 含左含右
        print(self.message)

    # step 8 --定义发送弹幕的方法
    def SendDanMu(self):
        # step 9 -- 定义发送弹幕方法的全局变量与参数    发送的信息 msg 为使用获取弹幕方法抓取到的最近10条弹幕后三条中随机一条
        self.urlSend = 'https://api.live.bilibili.com/msg/send'
        self.formSend = {   'color':'16777215',
                            'csrf_token':'e1577bd2347f0ca58c3055764a1a52a3',
                            'fontsize':'25',
                            'mode':'1',
                            'msg':self.message,
                            'rnd':'1525084816',
                            'roomid':self.roomid   }
        # step 10 -- 指定 Cookie 值参数，用于登录账号  字典形式存储
        self.cookie = {'Cookie':'l=v; finger=964b42c0; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1525062219; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1525084817; buvid3=22606B51-2E1E-4392-9F7C-4919D6B1C94B65585infoc; LIVE_BUVID=AUTO1715250622196755; sid=56g64yeo; fts=1525084730; DedeUserID=321797672; DedeUserID__ckMd5=9574ea85e9a3c98c; SESSDATA=b11052b4%2C1527676745%2C029ab795; bili_jct=e1577bd2347f0ca58c3055764a1a52a3; _dfcaptcha=d67eab33fb4dd88decb085c1d16bc7e2'}
        
        # step 11 -- 调用request的post方法发送弹幕   data  与  cookies 是关键字参数
        self.htmlSend = requests.post(self.urlSend, data = self.formSend, cookies = self.cookie)
        print(self.htmlSend)

####################### 调用启动 ###########################

# step 7 -- 实例化 DanMuSend 类

#danmuSend = DanMuSend(8259977)      # 这个对象其实就相当于self    所以也可以这样调用 DanMuSend.GetDanMu(danmuSend) -与下一行效果一样
#danmuSend.getDanMu()    # 执行获取弹幕方法

# step 12 -- 执行发送弹幕的方法
#danmuSend.SendDanMu()   # 执行发送弹幕方法

####################### 调用优化 ###########################

# step 13 -- 调用代码的优化
if __name__ == '__main__':                  # 判断是否本模块运行
    while True:                             # 循环多次发送
        danmuSend = DanMuSend(8259977)      # 实例化
        danmuSend.getDanMu()                # 获取弹幕
        danmuSend.SendDanMu()               # 发送弹幕
        time.sleep(random.randint(6,10))    # 暂停


####################### 附加知识 ###########################
''' Lambda 表达式与 map 函数的使用
f = lambda x:x*2        #  x 为变量名  x * 2 相当于方法体
a = map(f, [3,2,1])     #  map 函数，用于多个变量执行一个方法。 如左，相当于 3, 2, 1分别执行 f 表达式。 返回的是一个map对象：<map object at 0x056B3AB0>
print(list(a))          #  list方法，返回 a 对象的 list 形式。[6, 4, 2]    # map 具有惰性计算性质，只能使用一次，如再次使用a，a为空。 转换成list集合可以防止惰性
'''

''' __name__ 函数
       __name__ 是Python的关键字。 当该模块被其他模块调用时  表示当前的模块名
       当 DanMu.py 文件直接执行的时候  __name__ 等于 __main__
       当其他模块导入该模块的时候  __name__ 不等于 ___main__

       举例来说 如：第 13 步的 if __name__ == '__main__'写法。
            这就意味着本模块(DanMu.py)文件中，会执行if代码块中的语句，对弹幕类进行实例化并获取、发送
            但是如果在其他模块导入本模块(import DanMu.py)的时候。其他模块只会执行其他代码，如 anMuSend 类。但并不会执行第 13 步骤中的 类的实例化与方法的调用。
'''