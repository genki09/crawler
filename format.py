# -*- coding: utf-8 -*-

import requests as req
from lxml import etree

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}


def con_sx():
    r = req.get('http://wjw.shanxi.gov.cn/wjywl02/24821.hrh', headers=header)
    et = etree.HTML(r.text)
    text = et.xpath('//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[3]/div/p[1]/span/span/text()')
    text_num = et.xpath('//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[3]/div/p[1]/span/text()')
    print(text_num[0]+text[0]+text_num[1]+text_num[2]+text[1]+text_num[3]+text_num[4]+text[2]+'，'+text[4]+text_num[5])

con_sx()