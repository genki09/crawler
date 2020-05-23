# -*- coding: utf-8 -*-

import requests
from lxml import etree
import os


def get_from_artist():
    artist_name = 'Rembrandt'
    url = 'https://useum.org/artist/{}'.format(artist_name)
    r = requests.get(url).text
    et = etree.HTML(r)
    try:
        os.makedirs('/Users/apple/WebstormProjects/art/gallery/巴洛克式/{}'.format(artist_name))
    except:
        pass
    links = []
    res = []
    rea_name = []
    try:
        for i in range(1, 3):
            for j in range(1, 8):
                links.append(et.xpath('//*[@id="useum-tetris-artworks-ut"]/div[1]/div/ul[{}]/li[{}]/div[1]/a/@href'.format(i, j)))
    except:
        pass

    photo = et.xpath('//*[@id="block-useum-user-passport"]/div/div[2]/div[1]/img/@src')[0]
    r = requests.get(photo).content
    path = '/Users/apple/WebstormProjects/art/photos/{}.jpg'.format(artist_name)
    with open(path, 'wb') as f:
        f.write(r)
        print('已保存头像')

    for href in links:
        if bool(href):
            http = 'https://useum.org' + href[0]
            r = requests.get(http).text
            et = etree.HTML(r)
            link = et.xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div/div/div[1]/img[1]/@src')[0]
            name = et.xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div/div/div[3]/div[1]/div[2]/h1/text()')[0].strip(' \n\t\r')
            res.append(link)
            rea_name.append(name)
            print(link)
    for i in range(len(res)):
        r = requests.get(res[i])
        picture = r.content
        path = '/Users/apple/WebstormProjects/art/gallery/巴洛克式/{}/{}.jpg'.format(artist_name, rea_name[i])
        with open(path, 'wb') as f:
            f.write(picture)
            print('已保存')


def format_filename():
    path = '/Users/apple/WebstormProjects/art/gallery/巴洛克式/Rembrandt'
    files = []
    for root, dirs, file in os.walk(path):
        files = file

    arr = []
    for i in range(len(files)):
        if 'DS' in files[i]:
            i -= 1
            continue
        dic = {}
        dic["src"] = 'Rembrandt/' + files[i]
        dic["artist"] = 'Rembrandt'
        dic["name"] = files[i][:-4]
        arr.append(dic)

    with open('json.txt', 'w') as f:
        f.write(str(arr))
    # print(arr)


# get_from_artist()
format_filename()
