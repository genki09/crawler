# -*- coding:utf-8 -*-

import requests as req
import execjs
import time
from lxml import etree

# 创建对话框，便于在后续post与get时拥有同样的cookie
se = req.session()
# 获取本地时间，将以时间戳为标志创建对话
t = int(time.time() * 1000)
# 创建菜单及对应编号一览字典
dic = {}
# 定义用户名与密码
username = '07172336'
password = 'lll;;;'


def login():
    # 通过拼接URL获取验证码地址，储存到img.png
    h = se.get('http://202.119.206.62/jwglxt/kaptcha?time='+str(t))
    with open('img.png', 'wb') as f:
        f.write(h.content)

    # 在登陆页面的html文件中获取该时间戳与cookie下的csrftoken值
    h = se.get('http://202.119.206.62/jwglxt/xtgl/login_slogin.html')
    et = etree.HTML(h.text)
    csrt = et.xpath('//*[@id="csrftoken"]/@value')[0]

    # 动态获取RSA加密时的参数
    get_key = se.post('http://202.119.206.62/jwglxt/xtgl/login_getPublicKey.html?time='+str(t)).json()
    modulus = get_key.get("modulus")
    exponent = get_key.get("exponent")

    # 调取rsa.js文件中的getpwd函数对原始密码进行加密
    with open('rsa.js', encoding='utf-8') as f:
        jsdata = f.read()
    password_encrypt = execjs.compile(jsdata).call('getpwd', password, modulus, exponent)

    # 输入以获取POST参数中的'yzm'
    yzm = input("验证码：")

    # 定义发送参数
    data = {
        'csrftoken': csrt,
        'yhm': username,
        'mm': password_encrypt,
        'yzm': yzm
    }

    # 定义请求头
    login_headers = {
        'Referer': 'http://202.119.206.62/jwglxt/xtgl/login_slogin.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }

    # 与时间戳拼接出登陆网址，发送post登陆请求
    url = 'http://202.119.206.62/jwglxt/xtgl/login_slogin.html?time='+str(t)
    h = se.post(url, data=data, headers=login_headers)
    # print(h)

    data2 = {
        'xyyjtxb_id': '',
        'czdm': 'xs'
    }

    time.sleep(6)   # 按钮是5秒，这里休眠6秒
    h_check = se.post('http://202.119.206.62/jwglxt/xtgl/login_cxGxqrzt.html', data=data2)
    print(h_check.text)  # 若检查成功则会弹出"更新成功"
    h_in = se.get('http://202.119.206.62/jwglxt/xtgl/index_initMenu.html')  # 正式登陆进入功能主页面

    et = etree.HTML(h_in.text)
    menu = et.xpath('//*[@id="drop1"]/text()')
    for i in menu:
        if i == ' ':
            menu.remove(i)
    print(menu)

    for i in range(1, 7):
        menu_drop = et.xpath('//*[@id="cdNav"]/ul/li[{}]/ul/li/a/text()'.format(i))
        menu_drop_id = et.xpath('//*[@id="cdNav"]/ul/li[{}]/ul/li/a/@onclick'.format(i))

        d = {}
        j = 0
        for item in menu_drop_id:
            left = item.find('(')
            right = item.find(',')
            item = item[left+2:right-1]
            d[menu_drop[j]] = item
            j += 1
        dic[menu[i-1]] = d


'''
def sch_pdf():
    url = 'http://202.119.206.62/jwglxt/kbcx/' \
          'xskbcx_cxXskbcxIndex.html?gnmkdm={}&layout=default&su={}'.format(dic['信息查询']['学生课表查询'], username)
    r = se.get(url)
    # http://202.119.206.62/jwglxt/kbcx/xskbcx_cxXsShcPdf.html?doType=table'
    print(r)

    body = {
        'gndm': dic['信息查询']['学生课表查询']
    }
    url = 'http://202.119.206.62/jwglxt/xtgl/index_initMenu.html?jsdm=&_t='+str(t)
    head = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    r = se.post('http://202.119.206.62/jwglxt/xtgl/index_cxBczjsygnmk.html?gnmkdm=index&su=07172336', data=body, headers=head)
    print(r.text)
'''

if __name__ == '__main__':
    login()
