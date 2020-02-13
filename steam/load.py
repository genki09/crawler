# -*- coding:utf-8 -*-

import requests
import execjs
import time
import re
from lxml import etree

get_rsakey_url = 'https://store.steampowered.com/login/getrsakey/'
login_url = 'https://store.steampowered.com/login/dologin/'
login_headers = {
    'Referer': 'https://store.steampowered.com/login/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
}

game_headers = {'Accept-Language': 'zh-CN,zh;q=0.9', }

req = requests.session()
sign_dict = {'account_incorrect_sign': 1, 'guard_fail_sign': 1}


# 加密密码
def get_login_rsakey():
    # 第一次输入账号密码错误后，会被置0，应该在开始置1
    sign_dict['guard_fail_sign'] = 1

    username = input('input your steam account number:')
    password = input('input your steam account password:')

    data = {
        'donotcache': str(int(time.time() * 1000)),
        'username': username
    }
    getkey_html = req.post(get_rsakey_url, data=data, headers=login_headers).json()
    pub_mod = getkey_html.get('publickey_mod')
    pub_exp = getkey_html.get('publickey_exp')
    timestamp = getkey_html.get('timestamp')
    # 加密密码 RSA
    with open('rsa.js', encoding='utf-8') as f:
        jsdata = f.read()
    password_encrypt = execjs.compile(jsdata).call('getpwd', password, pub_mod, pub_exp)
    return username, password_encrypt, timestamp


# 发送登录信息
def login_request(_data_):
    login_data = {'donotcache': str(int(time.time() * 1000)),
                  'username': _data_[0],
                  'password': _data_[1],
                  'twofactorcode': '',
                  'emailauth': '',
                  'loginfriendlyname': '',
                  'captchagid': '-1',
                  'captcha_text': '',
                  'emailsteamid': '',
                  'rsatimestamp': _data_[2],
                  'remember_login': 'false',
                  }

    response_data = req.post(login_url, data=login_data, headers=login_headers).json()

    if response_data['message']:
        print('\nlogin extra information:', response_data['message'], '\n')
    else:
        print('\nlogin extra information:', None, '\n')
    return response_data, login_data


# 输入手机令牌
def input_guard_number(_data_):
    html_data = _data_[0]
    login_data = _data_[1]
    # 没有手机令牌的账号，在输入过邮箱令牌一次后可以直接登录
    if (html_data.get('success') == True) and (html_data.get('login_complete') == True):
        sign_dict['guard_fail_sign'] = 0
        sign_dict['account_incorrect_sign'] = 0
        return html_data
    # 没有手机令牌，第一次登录需要邮箱验证码
    elif html_data.get('emailauth_needed') == True:
        email_guard_number = input('input the email guard number:')
        login_data['twofactorcode'] = email_guard_number
        sign_dict['account_incorrect_sign'] = 0
        return req.post(login_url, data=login_data, headers=login_headers).json()
    # 输入手机令牌
    elif (html_data.get('success') == False) and (html_data.get('message') == ''):
        phone_guard_number = input('input the phone guard number:')
        login_data['twofactorcode'] = phone_guard_number
        sign_dict['account_incorrect_sign'] = 0
        return req.post(login_url, data=login_data, headers=login_headers).json()
    # 输入账号密码错误
    elif (html_data.get('success') == False) and (
            html_data.get('message') == 'The account name or password that you have entered is incorrect.'):
        sign_dict['guard_fail_sign'] = 0
        print('\nthe input incorrect !!! try again\n')


# 判断是否登录成功
def if_login_successful(login_with_guard_html):
    if login_with_guard_html != None:
        if (login_with_guard_html.get('success') == True) and (login_with_guard_html.get('login_complete') == True):
            sign_dict['guard_fail_sign'] = 0
            print('\nsuccessfully login')


# 登陆
def login():
    # 账号密码错误，重新输入账号密码
    while (bool(sign_dict['account_incorrect_sign'])):
        data = get_login_rsakey()
        data2 = login_request(data)
        # 令牌输入错误，重新输入令牌
        while (bool(sign_dict['guard_fail_sign'])):
            html_data = input_guard_number(data2)
            if_login_successful(html_data)


# 登陆后在主页获取个人页面URL
def get_personal_url():
    r = req.get('https://store.steampowered.com/')
    et = etree.HTML(r.text)
    url_person = et.xpath('//*[@id="global_actions"]/a')
    url_person = url_person[0].attrib.get('href')
    return url_person


# 通过个人页面URL获取已购买游戏的字典
def get_game_list(url_person):
    r = req.get(url_person + 'games/?tab=all', headers=game_headers)
    et = etree.HTML(r.text)
    game_list_info = et.xpath('//*[@language="javascript"]/text()')
    game_list = game_list_info[0].strip('\n\t')
    game_list_dict = game_list[game_list.find('['):game_list.find(']') + 1]
    game_list_dict = eval(game_list_dict.replace('true', '1').replace('false', '0'))

    dict = {}
    dict2 = {}

    for item in game_list_dict:
        if item.get('hours_forever', False):
            dict2['hours_forever'] = float(item['hours_forever'])
        else:
            dict2['hours_forever'] = 0
        if item.get('last_played', False):
            timeArray = time.localtime(item['last_played'])
            Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            dict2['last_played'] = Time
        else:
            dict2['last_played'] = 'no data'

        dict2['store_url'] = 'https://store.steampowered.com/app/' + str(item['appid'])

        dict[item['name']] = dict2
        dict2 = {}

    return dict


# 通过个人页面URL获取账号好友的字典
def get_friends(url_person):
    r = req.get(url_person + 'friends/')
    et = etree.HTML(r.text)
    list_gaming_game = et.xpath('//*[@class="selectable friend_block_v2 persona in-game "]/div[3]/span/span/text()')
    list_gaming_gamer = et.xpath('//*[@class="selectable friend_block_v2 persona in-game "]/div[3]/text()')
    x = []
    for i in range(0, len(list_gaming_gamer), 3):
        x.append(list_gaming_gamer[i])
    list_gaming_gamer = x

    list_online_gamer = et.xpath('//*[@class="selectable friend_block_v2 persona online "]/div[3]/text()')
    x = []
    for i in range(0, len(list_online_gamer), 3):
        x.append(list_online_gamer[i])
    list_online_gamer = x

    list_offline_time = et.xpath('//*[@class="selectable friend_block_v2 persona offline "]/div[3]/span[2]/text()')
    for i in range(len(list_offline_time)):
        list_offline_time[i] = list_offline_time[i].strip('\n\r\t')
    list_offline_gamer = et.xpath('//*[@class="selectable friend_block_v2 persona offline "]/div[3]/text()')
    x = []
    for i in range(0, len(list_offline_gamer), 4):
        x.append(list_offline_gamer[i])
    list_offline_gamer = x

    dict = {}
    if bool(list_gaming_gamer):
        for i in range(len(list_gaming_gamer)):
            dict[list_gaming_gamer[i]] = 'in-game: {}'.format(list_gaming_game[i])
    if bool(list_online_gamer):
        for i in range(len(list_online_gamer)):
            dict[list_online_gamer[i]] = 'online'
    for i in range(len(list_offline_gamer)):
        dict[list_offline_gamer[i]] = 'offline: {}'.format(list_offline_time[i])

    return dict


# 通过游戏URL访问商店页面获取该游戏的其他信息
def get_app_info(url):
    r = req.get(url, headers=game_headers)
    et = etree.HTML(r.text)

    if bool(et.xpath('//*[@id="game_highlights"]/div[1]/div/div[4]/div/div[2]/a/text()')):
        pass
    else:
        data = {'sessionid': 'e313b9be4c02b40aed87c756', 'ageDay': '1', 'ageMonth': 'January', 'ageYear': '2000'}    # 'sessionid': 'e313b9be4c02b40aed87c756'
        r = requests.post(r.url, data=data, headers=game_headers)
        r = requests.get(url, headers=game_headers)
        et = etree.HTML(r.text)

    # s_id = et.xpath()

    list_app_tag = et.xpath('//*[@id="game_highlights"]/div[1]/div/div[4]/div/div[2]/a/text()')
    for i in range(len(list_app_tag)):
        list_app_tag[i] = list_app_tag[i].strip('\n\r\t')

    assess_app_percent = et.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/span[3]/text()')
    assess_app_percent = float(re.findall('(\d+)', assess_app_percent[0].strip('\n\r\t'))[-1]) / 100

    assess_app = et.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/span[1]/text()')[0]

    list_developers = et.xpath('//*[@id="developers_list"]/a/text()')
    list_subtitles = et.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[5]/div[2]/a/text()')

    dict = {}
    dict['tap'] = list_app_tag
    dict['assess_app_percent'] = assess_app_percent
    dict['assess_app'] = assess_app
    dict['developers'] = list_developers
    dict['subtitles'] = list_subtitles
    return dict


if __name__ == '__main__':
    login()
    # url1 = 'https://store.steampowered.com/app/220440'
    # url = 'https://store.steampowered.com/agecheck/app/220440'

    url_person = get_personal_url()

    # url_person = 'https://steamcommunity.com/id/yqjiejie/'

    game_dict = get_game_list(url_person)

    for i in game_dict:
        flag = True
        while flag:
            try:
                game_dict[i].update(get_app_info(game_dict[i]['store_url']))
                flag = False
            except:
                print('unknown mistakes appeared..trying again..')
                time.sleep(1)
                flag = True

        print('{},{},{},{},{},{},{},{},{}'.format(i, game_dict[i]['hours_forever'], game_dict[i]['last_played'],
                                                  game_dict[i]['store_url'],game_dict[i]['tap'], game_dict[i]['assess_app_percent'],
                                                  game_dict[i]['assess_app'],game_dict[i]['developers'], game_dict[i]['subtitles']))

        # print(i, game_dict[i])
    # print(game_dict)

    # print(get_friends(url_person))
