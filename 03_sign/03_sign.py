'''
使用Python的GUI图形化界面设计桌面应用程序
点击按钮爬取对应签名并返回到桌面应用程序界面
        2018年5月1日13:36:51
'''
############################# 前期准备 #############################
'''GUI图形化界面
Tkinter是Python的标准GUI库。Python使用Tkinter可以快速的创建GUI应用程序
Tkinter比较简单、简陋。
'''

############################# 桌面开发 #############################
# step 1 -- 导包
from tkinter import *       # * 只能导入 __all__ 中的东西，即tkinter的__init__中
from tkinter import messagebox
import requests             # 请求
import re                   # 正则表达式
from PIL import Image, ImageTk  # 显示图片

# step 10 -- 点击按钮 执行downLoad方法  模拟浏览器发送POST请求
def downLoad():
    startURL = 'http://www.uustv.com/'
    name = entry.get().strip()      # 获取输入框中的内容  -- 姓名     并去除两端空格
    if(name == ''):
        messagebox.showinfo('提示', '请输入用户名')
    else:
        data = {
            'fontcolor':'#000000',
            'fonts':'jfcs.ttf',
            'sizes':'60',
            'word':name 
        }
        result = requests.post(startURL, data = data)
        result.encoding = 'UTF-8'
        #print(result)       # 获取请求状态

        # step 11 -- 获取网站源码 响应Json解析 提取最终返回的图片
        html = result.text
        #print(html)         # 网站源码
        reg = '<div class="tu">.*?<img src="(.*?)"/></div>'      # 正则匹配 --网页展示签名结果图片的div
        imagePath = re.findall(reg,html)
        #print(imagePath)     # 图片路径（相对路径）

        # step 12 -- 获取图片完整路径
        imgURL = startURL + imagePath[0]

        # step 13 -- 保存图片     参数： 字符串形式.字符串格式化， 二进制文件的方式写入(若存在则覆盖，不存在则创建)
        response = requests.get(imgURL).content     # 获取图片内容
        f = open('{}.gif'.format(name),'wb')
        #with open('{}.gif'.format(name),'wb') as f
        f.write(response)

        # step 14 -- 显示图片到GUI
        bm = ImageTk.PhotoImage(file = '{}.gif'.format(name))
        lable2 = Label(root, image = bm)
        lable2.bm = bm
        lable2.grid(row = 2, columnspan = 2)

# step 2 -- 创建窗口
root = Tk()

# step 3 -- 标题
root.title('python - 签名设计')

# step 4 -- 调整窗口  （宽x高）  --小写的x
root.geometry('600x300')
# step 5 -- 调整窗体初始位置   （相对屏幕左上角）
root.geometry('+640+300')

# step 6 -- 标签控件  关键字参数名称不可随意更改
lable = Label(root, text = '签名', font = ('华文行楷', 20), fg = 'red')
# step 7 -- 标签定位  -- 三种方式：grid  pack  place
lable.grid()    # 默认第 0 行 第 1 列

# step 8 -- 输入框控件  定位 （第 0 行 第 1 列）
entry = Entry(root, font = ('微软雅黑', 20))
entry.grid(row = 0, column = 1)

# step 9 -- 按钮空间  定位 （第 1 行 第 0 列）  command：-- 关键字参数  点击按钮执行的事件  downLoad() -- 自定义方法名，点击按钮需要执行的方法
button = Button(root,text = '获取', font = ('微软雅黑', 20), command = downLoad)
button.grid(row = 1, column = 0)

############################# 网页爬虫 #############################

############################# 爬虫准备 #############################

'''
    以 http://www.uustv.com/ 网站为例
    打开开发者工具，进入"网络"选项卡，点击"马上给我设计"，获取到很多请求信息，进入第一条。
        消息头：
            请求网址：http://www.uustv.com/
            请求方式：POST
        参数：
            word：          -- 提交的姓名
            sizes：60       -- 字体大小
            fonts：         -- 字体
            fontcolor：     -- 字体颜色
'''




# step last -- 消息循环  显示窗口
root.mainloop()
