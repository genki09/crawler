# -*- coding: utf-8 -*-

import requests as req
from lxml import etree
import timeout_decorator

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}


def yunan():
    url = 'http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731'
    r = req.get(url)
    et = etree.HTML(r.text)
    lines_titles = et.xpath('/html/body/div[4]/div[2]/div[2]/ul/li/a/text()')
    lines_dates = et.xpath('/html/body/div[4]/div[2]/div[2]/ul/li/span/text()')
    lines_urls = et.xpath('/html/body/div[4]/div[2]/div[2]/ul/li/a/@href')

    for i in range(len(lines_titles)-5):
        lines_urls[i] = 'http://ynswsjkw.yn.gov.cn' + lines_urls[i]
        if '疫情情况' in lines_titles[i]:
            print(lines_titles[i], '\t', lines_dates[i], '\t', lines_urls[i], '\t', i)

    return lines_urls


def shanxi():
    url = 'http://wjw.shanxi.gov.cn/wjywl02/index.hrh'
    r = req.get(url, headers=header)
    et = etree.HTML(r.text)
    lines_titles = et.xpath('//*[@id="container"]/div[3]/div[3]/div[2]/ul/li/a/text()')
    lines_dates = et.xpath('//*[@id="container"]/div[3]/div[3]/div[2]/ul/li/span/text()')
    lines_urls = et.xpath('//*[@id="container"]/div[3]/div[3]/div[2]/ul/li/a/@href')

    for i in range(len(lines_titles)-10):
        if '疫情情况' in lines_titles[i] or '轨迹' in lines_titles[i]:
            print(lines_titles[i], '\t', lines_dates[i], '\t', lines_urls[i], '\t', i)

    return lines_urls


@timeout_decorator.timeout(30)
def con_yn():
    lines_urls = yunan()

    print('-------------------------------------------------------------------')
    n = int(input("云南第几条新闻？"))
    print('-------------------------------------------------------------------')

    r = req.get(lines_urls[n])
    et = etree.HTML(r.text)
    text = et.xpath('//*[@id="content"]/p[1]/span/text()')
    print(''.join(text))
    # print(text[8])


@timeout_decorator.timeout(30)
def con_sx():
    lines_urls = shanxi()

    print('-------------------------------------------------------------------')
    n = int(input("山西第几条新闻？"))
    print('-------------------------------------------------------------------')

    r = req.get(lines_urls[n], headers=header)
    et = etree.HTML(r.text)
    text = et.xpath('//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[3]/div/p[1]/span/span/text()')
    text_num = et.xpath('//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[3]/div/p[1]/span/text()')
    if bool(text) and bool(text_num):
        print(text_num[0]+text[0]+text_num[1]+text_num[2]+text[1]+text_num[3]+text_num[4]+text[2]+'，'+text[4]+text_num[5])
    elif bool(text) or bool(text_num):
        print(''.join(text_num))
        print(''.join(text))
    #print(text_num)
    #print(text)


if __name__ == '__main__':
    flag = True
    while flag:
        try:
            con_sx()
            print('-------------------------------------------------------------------')
            con_yn()
            print('-------------------------------------------------------------------')
            flag = False
        except Exception as e:
            print(e)
