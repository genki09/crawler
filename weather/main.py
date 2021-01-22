# -*- coding:utf-8 -*-

import json
import requests
from xpinyin import Pinyin
from lxml import etree


def get_name_pm_form_meizu(cityid):
    api_url = "http://aider.meizu.com/app/weather/listWeather?cityIds={}".format(cityid)
    r = requests.get(api_url).content.decode('utf-8')
    info = json.loads(r)
    pm25 = info['value'][0]['pm25']['aqi']
    cityname = info['value'][0]['city']
    if cityname and pm25:
        return cityname, pm25
    else:
        print('魅族api错误')
        return 0, 0


def get_citypinyin_from_gaode(lat, lon):
    url = 'http://restapi.amap.com/v3/geocode/regeo?key=～高德Web服务api～&location={:.4f},{:.4f}&poitype=&radius=&extensions=base&batch=false&roadlevel=0'.format(lon, lat)
    r = requests.get(url).text
    rt = json.loads(r)
    # print('经纬度信息为：{:.4f}, {:.4f}'.format(lon, lat))
    cityall = rt['regeocode']['addressComponent']['city']
    if cityall:
        if '市' in cityall:
            cityname = cityall.strip('市')
        citypinyin = Pinyin().get_pinyin(cityname, '')
        return cityall, citypinyin
    else:
        print('位置错误')
        return 0, 0


def get_cityid_form_chinaweather(cityall, citypinyin):
    url = 'http://flash.weather.com.cn/wmaps/xml/{}.xml'.format(citypinyin)
    r = requests.get(url).content.decode('utf-8')
    et = etree.XML(r)
    res = et.xpath('/*/city[@cityname="{}"]/@url'.format(cityall))
    if res:
        return res[0]
    else:
        resall = et.xpath('/*/city/@url')
        if resall:
            print('错误4')
            return resall[0]
        else:
            print('请求全部cityid出错')
            return 0
    # print(et.xpath('/*/city/@url'))


def main(lat, lon):
    cityall, citypinyin = get_citypinyin_from_gaode(lat, lon)
    if cityall and citypinyin:
        cityid = get_cityid_form_chinaweather(cityall, citypinyin)
        if cityid:
            name, pm = get_name_pm_form_meizu(cityid)
            if name and pm:
                print('{}的pm2.5指数现在为{}'.format(name, pm))
            else:
                print('错误1')
        else:
            print('错误2')
    else:
        print('错误3')


if __name__ == '__main__':
    # main(34.2172, 119.1364)
    have = str(input())
    have = have.split(', ')
    lat, lon = float(have[0]), float(have[1])
    main(lat, lon)
