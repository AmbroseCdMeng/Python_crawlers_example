'''
   12306 验证码登录
        url：http://www.12306.cn/mormhweb/
        
        2018年5月13日16:55:21

    12306 登录流程 -- 浏览器
        1、进入登录页面      https://kyfw.12306.cn/otn/login/init
        2、填写用户名密码
        3、操作验证码
        4、提交             
        5、检测验证码       提交验证码时使用的 Get， 提交用户名密码时使用的 Post
        6、检测用户名密码
'''

import requests

# cookie 保持
#       直接使用request发送请求时 
#       会发现 校验结果提示 "验证码校验失败  信息为空"
#       这是因为下载的验证码图片与提交的验证信息 无直接联系 
#       所以需要在开始保持 cookie 然后下载和提交都使用同一个 session 对象发送请求
#       此时会发现 校验结果提示变为 "验证码校验失败"
#       这是因为我们选择的坐标目前是固定的值 所以校验失败

#       因为目前我们不准备实现图片的自动识别 这涉及到机器学习 难度较大 所以这里我们暂时使用手动输入验证结果坐标的方法
session = requests.Session()


# 下载验证码
#       通过开发者工具抓包可以发现，验证码是一张图片
#       请求的方式为 Get 
#       请求地址为 https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.07726311250013973
captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.07726311250013973'
# 发送请求
# response = requests.get(captcha_url)
response = session.get(captcha_url)
# 输出请求的状态码
# print(response.status_code)
# 输出请求结果的二进制信息（图片本身是二进制信息）
# print(response.content)
# 将二进制文件写入图片
fb = open('05_captcha.jpg', 'wb')
fb.write(response.content)
fb.close()


# 检测验证码
#       通过开发者工具抓包可以发现，检测验证码的信息名为 captcha-check
#       请求的方式为 Post
#       请求地址为 https://kyfw.12306.cn/passport/captcha/captcha-check
#       cookies  --用户名密码以及验证码图片等信息
#       FormData --验证码的选择结果 选中位置相对于图片左上角的坐标
captcha_check_api = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
# 手动输入验证码的坐标
code = input('请输入验证码的坐标>>>:')  # 纵坐标需要减去图片头的 30 像素
data = {
    'answer': code.split(),
    'login_site': 'E',
    'rand': 'sjrand'
}
# check_response = requests.post(captcha_check_api, data=data)    # 返回 Json 对象
check_response = session.post(captcha_check_api, data=data)
check_response.encoding = 'UTF-8'
print(check_response.text)

# 到1小时的地方，由于网络问题