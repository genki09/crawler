# -*- coding: utf-8 -*-

import requests
import json
import pandas as pd
from lxml import etree
import time
import csv
import sys
import os
from math import sqrt
from xpinyin import Pinyin


def get_lines(cityE, city):
    lst = []
    for i in range(1, 10):
        url = 'http://{}.gongjiao.com/lines_{}.html'.format(cityE, i)
        time.sleep(1)
        print('Searching for lines starting with {}..'.format(i))
        r = requests.get(url).text
        et = etree.HTML(r)
        line = et.xpath('//div[@class="list"]//a/text()')
        for l in line:
            lst.append(l.split(city)[1])
    return lst


def get_dt(city, line):
    url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key=b61d59a306da2b4620e583d129da82fa&output=ison&city={}&offset=1&keywords={}&platform=JS'.format(
        city, line
    )
    r = requests.get(url).text
    rt = json.loads(r)

    try:
        if rt['buslines']:
            print('data avaliable..')
            if not len(rt['buslines']):
                print('no data in list..')
            else:
                dt = {'line_name': rt['buslines'][0]['name'],
                      'polyline': rt['buslines'][0]['polyline'],
                      'total_price': rt['buslines'][0]['total_price']}

                st_name = []
                st_coords = []

                for st in rt['buslines'][0]['busstops']:
                    st_name.append(st['name'])
                    st_coords.append(st['location'])

                dt['station_name'] = st_name
                dt['station_coords'] = st_coords

                dm = pd.DataFrame([dt])
                # print(dm)
                dm.to_csv('bus/result/{}_lines.csv'.format(cityE), mode='a', header=False)
        else:
            pass
    except:
        print('error..')
        time.sleep(2)
        get_dt(city, line)


def write_chart(cityE):
    origin = sys.stdout
    f = open('bus/result/info_{}.csv'.format(cityE), 'w')
    sys.stdout = f  # 以write方式打开创建并编辑新文件st.csv，使标准输入流流入该文件，并暂时存放标准输入流到origin中

    csvfile = csv.reader(open('bus/result/{}_lines_norepeat.csv'.format(cityE)))
    for data in csvfile:
        print(data[5])  # 打开原始爬虫数据表，读取第六列，即各站位置坐标数据

    sys.stdout = origin
    f.close()  # 关闭文件，st.csv文件编辑完毕，现在文件内都是原始的坐标字符串文件，将标准输入流归还

    f = open('bus/result/info_{}.csv'.format(cityE), 'r')
    lines = f.readlines()
    f.close()  # 以read方式打开st.csv文件，将里面全部的数据按行存入lines中，关闭文件

    origin = sys.stdout
    f = open('bus/result/info_{}.csv'.format(cityE), 'w')
    sys.stdout = f  # 以write方式打开创建并编辑新文件，使标准输入流流入该文件，并暂时存放标准输入流到origin中

    csvfile = csv.reader(open('bus/result/{}_lines_norepeat.csv'.format(cityE)))
    for data in csvfile:
        print(data[4])  # 打开原始爬虫数据表，读取第五列，即各站名称

    sys.stdout = origin
    f.close()  # 关闭文件，站点名称文件编辑完毕，现在文件内都是原始的坐标字符串文件，将标准输入流归还

    f = open('bus/result/info_{}.csv'.format(cityE), 'r')
    lines_c = f.readlines()
    f.close()  # 以read方式打开st.csv文件，将里面全部的数据按行存入lines中，关闭文件

    origin = sys.stdout
    f = open('bus/result/info_{}.csv'.format(cityE), 'w')
    sys.stdout = f  # 以write方式打开创建并编辑文件，使标准输入流流入该文件，并暂时存放标准输入流到origin中

    csvfile = csv.reader(open('bus/result/{}_lines_norepeat.csv'.format(cityE)))
    for data in csvfile:
        print(data[1])  # 打开原始爬虫数据表，读取第二列，即路线名称数据

    sys.stdout = origin
    f.close()  # 关闭文件，st_n.csv文件创建完毕，现在文件内都是原始的站路名称数据，将标准输入流归还

    f = open('bus/result/info_{}.csv'.format(cityE), 'r')
    lines_n = f.readlines()
    f.close()  # 以read方式打开编辑好的文件，将所有的数据存入lines_n中，关闭文件

    origin = sys.stdout  # 每次互相交换之间只能有一个print()
    f = open('bus/result/info_{}.csv'.format(cityE), 'w')
    sys.stdout = f  # 以write方式再次打开文件，上几次只为存放数据，本次打开是因为不想再新建一个文件进行编辑，将原有文件抹除重新编辑，反正之前的数据已经存入到了lines中，交换标准输出流

    di = {}  # 新建di字典，准备存放站点位置最终结果
    di_c = {}  # 新建di_c字典，准备存放站点名称最终结果
    dict = {}   # 目的是利用字典中键不能重复的特性来组成一个不会重复站名的字典
    dict_st = {}    # 存放所有站的全部位置信息
    lines_list = []  # 以列表形式存放行信息
    name = []   # 以列表形式存放站名

    print('id,station_name,lines_name,x,y,order')  # 在再次打开并准备写入数据的时候，文件内容已被抹除，在文件第一行写上csv表格的列名

    for l in range(len(lines)):
        li = lines[l].strip('[\n]').strip('\'')
        li = li.split('\', \'')  # 将lines内容格式化为列表，以便之后存入字典中

        li_n = lines_n[l].strip('\n')
        li_n = li_n[:li_n.find('(')]  # 读取并留下第一个括号前的所有字符，即读取出线路名称存入li_n中，

        li_c = lines_c[l].strip('[\n]').strip('\'')
        li_c = li_c.split('\', \'')  # 将lines_c内容格式化为列表，以便之后存入字典中

        di[l] = li
        di_c[l] = li_c

        for i in range(len(di[l])):
            fin = di[l][i].split(',')
            fin[0] = float(fin[0])
            fin[1] = float(fin[1])
            # print('{},{},{},{},{},{}'.format(l, di_c[l][i], li_n, fin[0], fin[1], i+1))
            dict[di_c[l][i]] = di[l][i]
            lines_list.append([l, di_c[l][i], li_n, fin[0], fin[1], i+1])

    for i in dict:
        name.append(i)
    for i in range(len(name)):
        dict_st[name[i]] = []
    for i in dict_st.keys():
        for j in range(len(lines_list)):
            if i == lines_list[j][1]:
                dict_st[i].append([lines_list[j][3], lines_list[j][4]])
    # print(dict_st)    # 打印站名-站点所有位置表

    for i in dict_st:
        dict_st[i] = cal_avg(dict_st[i])
    # print(dict_st)    # 打印站名-站点形心位置（一个）表

    for i in range(len(lines_list)):
        x_c = dict_st[lines_list[i][1]][0]
        y_c = dict_st[lines_list[i][1]][1]
        
        if sqrt((lines_list[i][3]-x_c)**2+(lines_list[i][4]-y_c)**2) < 0.003:    # 这个数字越大，允许同名站之间的距离就越大（误差越大）
            print('{},{},{},{},{},{}'.format(lines_list[i][0], lines_list[i][1], lines_list[i][2],
                                         x_c, y_c, lines_list[i][5]))
        else:
            print('{},{},{},{},{},{}'.format(lines_list[i][0], lines_list[i][1], lines_list[i][2],
                                         lines_list[i][3], lines_list[i][4], lines_list[i][5]))

    sys.stdout = origin
    f.close()  # 最终结果已以标准输出方式存入文件中，关闭文件，交换标准输入流


def del_rep(readDir, cityE):
    norepeat = "bus/result/{}_lines_norepeat.csv".format(cityE)
    lines_seen = set()
    outfile = open(norepeat, "w")
    readfile = open(readDir, "r")
    for line in readfile:
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    readfile.close()


def cal_avg(list_xy):
    n = len(list_xy)
    x = y = 0
    if n == 1:
        x = float(list_xy[0][0])
        x = float('%.6f' % x)
        y = float(list_xy[0][1])
        y = float('%.6f' % y)
        fin = [x, y]
    else:
        for i in range(n):
            x += float(list_xy[i][0])
            y += float(list_xy[i][1])
        x = x / n
        x = float('%.6f' % x)
        y = y / n
        y = float('%.6f' % y)
        fin = [x, y]
    return fin


if __name__ == "__main__":
    t1 = time.time()
    city = '徐州'
    cityE = Pinyin().get_pinyin(city, '')
    # '''
    try:
        f = open('bus/result/{}_lines.csv'.format(cityE), 'r+')
        f.truncate()
        f.close()
    except:
        pass

    lines_list = get_lines(cityE, city)
    # print(lines_list)

    for i, line in enumerate(lines_list):
        print('id_{}:{}     '.format(i, line))
        get_dt(city, line)

    readDir = "bus/result/{}_lines.csv".format(cityE)
    del_rep(readDir, cityE)
    # '''
    write_chart(cityE)

    os.remove(readDir)

    t2 = time.time()
    print('耗时{}秒'.format(float('%.6f' % (t2 - t1))))

# b61d59a306da2b4620e583d129da82fa
# 81462cd792233fa4e494f7b4e58a1321
