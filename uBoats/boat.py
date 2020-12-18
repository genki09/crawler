# -*- coding: utf-8 -*-

import requests as req
import sys

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}


# 下载html页面为txt函数
def get_html_context(sea_location):
    url = 'https://www.uboat.net/maps/{}.htm'.format(sea_location)
    r = req.get(url, headers=header)

    origin = sys.stdout
    txt_name = 'html_{}.txt'.format(sea_location)
    f = open('html/' + txt_name, 'w')

    sys.stdout = f
    print(r.content.decode('utf-8'))
    sys.stdout = origin
    f.close()


# 筛选html文本文件的内容，并清洗部分数据
def select_from_txt(sea_location):
    con = []
    txt_name = 'html_{}.txt'.format(sea_location)
    f = open('html/' + txt_name)
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for line in f.readlines():
        if line.find('var marker') == 0:
            line = line.replace('var marker = L.marker(', '').replace('{icon: iconFate}).addTo(mymap).bindPopup(\'', '')
            line = line.replace('\');', '').strip(' ').strip('.')
            if not 0 < line.find('<strong>') < 20 and line[line.find('], ') + 3] not in nums:
                con.append(line)
    f.close()

    f = open('result/' + sea_location + '_lines.csv', 'w')
    f.writelines(con)


def final(sea_lists):
    for seaName in sea_lists:
        get_html_context(seaName)
        select_from_txt(seaName)


if __name__ == '__main__':
    all_seas = ["cape_farewell", "canaries", "cape_verde", "caribbean", "barents", "channel", "north_sea", "irish_sea",
                "kattegat", "south_atlantic", "black_sea", "baltic_sea", "us_east_coast", "biscay", "gibraltar",
                "mediterranean"]
    final(all_seas)
