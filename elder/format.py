# -*- coding: utf-8 -*-

import requests as req
from lxml import etree
import time
import json

header = {
'Host': '45.113.201.36',
'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'Accept': '*/*',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
'Referer': 'http://45.113.201.36/user.html',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': 'session=eyJ1aWQiOiI3MTIyNzM1In0.X5Pf8w.6qQ8bKHqe60LkgkLHGwoNVDkq_Q; role=ee11cbb19052e40b07aac0ca060c23ee'
}


def get_yanglao_from_web(art_num):
    url = 'http://mz.xz.gov.cn/public/article/{}'.format(art_num)
    r = req.get(url, headers=header).text
    et = etree.HTML(r)
    print(
        et.xpath('/html/body/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[6]/text()')[0].replace('\r\n', '').replace('\t',
                                                                                                                  ''))
    for i in range(3, 44):
        print(et.xpath('/html/body/div[2]/div[2]/div[1]/table/tbody/tr[{}]/td[6]/text()'.format(i))[0].replace('\r\n', '').replace(
            '\t', ''))


def decode_geo():
    fin_list = []
    con = 1
    for pages in range(1, 26):
        url = 'https://restapi.amap.com/v3/place/text?key=～高德Web服务api～&keywords=学院&types=&city=徐州' \
              + '&children=1&offset=&page=' + str(pages) + '&extensions=all'
        r = req.get(url, headers=header).text
        rt = json.loads(r)
        for x, i in enumerate(rt['pois']):
            f = i['location'].split(',')
            fin_list.append({
                'id': str(711 + con),
                'loc_name': i['name'],
                'lon': f[0],
                'lat': f[1]
            })
            con += 1
    print(fin_list)

# bilibili1024程序员节中一道题需要猜一个数字的工具函数，与elder项目无关
def bilibili1024():
    for i in range(1, 100000):
        url = 'http://45.113.201.36/api/ctf/5?uid={}'.format(i+100336889)
        r = req.get(url, headers=header).text
        rt = json.loads(r)
        print(str(i) + '失败 ' + str(rt['code']))
        if int(rt['code']) == 200:
            print(i+100336889)
            break

# art_list = [19598, 19596, 19595]
# for i in art_list:
#     get_yanglao_from_web(i)

# decode_geo()


bilibili1024()
