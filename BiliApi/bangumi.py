# -*- coding:utf-8 -*-

import json
import requests
import time
import sys
import os
import emailSender


def get_bangumis_info_relative(seed_id):
    # 通过种子season_id获取其所有相关番剧的id及其他信息
    bangumi_dict = {}
    for i in range(5):  # 这样大概率能添加上种子番剧的相关信息
        api_url = 'https://api.bilibili.com/pgc/web/recommend/related/recommend?season_id={}&from_pc=1'.format(seed_id)
        r = requests.get(api_url).content.decode('utf-8')
        info = json.loads(r)
        bangumi = info['result']['season']
        for item in bangumi:
            bangumi_dict[item['season_id']] = {'badge': item['badge'], 'new_ep': item['new_ep']['index_show'],
                                               'rating': item['rating'], 'title': item['title'],
                                               'season_type': item['season_type'], 'stat': item['stat']}
        seed_id = list(bangumi_dict.keys())[i]

    # print(bangumi_dict)

    # json.dump(bangumi_dict, open('temp.json', 'w', encoding='UTF-8'), ensure_ascii=False)   # 为了看清json格式将对象写到文件里再格式化


def get_from_av(aid):
    detail = {}
    api_url = 'http://api.bilibili.com/archive_stat/stat?aid={}'.format(aid)
    r = requests.get(api_url).content.decode('UTF-8')
    properties = json.loads(r)
    detail['view'] = properties['data']['view']
    detail['danmaku'] = properties['data']['danmaku']
    detail['reply'] = properties['data']['reply']
    detail['coin'] = properties['data']['coin']
    detail['share'] = properties['data']['share']
    detail['like'] = properties['data']['like']
    return detail


def get_part_info(season_id):
    container = {}
    information = {}
    api_url = 'https://www.biliplus.com/api/bangumi?season={}'.format(season_id)
    r = requests.get(api_url).content.decode('UTF-8')
    properties = json.loads(r)
    for item in properties['result']['episodes']:
        information[item['index']] = {'aid': item['av_id']}
        information[item['index']].update(get_from_av(item['av_id']))
        container.update(information)
    return container


def get_from_md(media_id):
    bangumi_info = {media_id: {}, 'part': {}}
    media = {}
    api_url = 'http://api.bilibili.com/pgc/view/web/media?media_id={}'.format(media_id)
    r = requests.get(api_url).content.decode('UTF-8')
    properties = json.loads(r)
    media['title'] = properties['result']['title']
    media['follow'] = properties['result']['stat']['series_follow']
    if bool(properties['result'].get('rating', 0)):
        media['score'] = properties['result']['rating']['score']
        media['count'] = properties['result']['rating']['count']
    else:
        media['score'] = 0
        media['count'] = 0
    media['ssid'] = properties['result']['season_id']
    bangumi_info[media_id].update(media)
    bangumi_info['part'].update(get_part_info(properties['result']['season_id']))
    # json.dump(bangumi_info, open('temp.json', 'w', encoding='UTF-8'), ensure_ascii=False)
    return bangumi_info


def filename_according_time():
    filetime = str(time.strftime('%m_%d$%H', time.localtime(time.time())))
    fileway = '{}.csv'.format(filetime)
    file_final = 'bangumi_4_2020/' + fileway
    return fileway, file_final


def write_chart(mdid, info_dic, file_final):
    origin = sys.stdout
    f = open(file_final, 'a+')
    sys.stdout = f
    #   输出属性行
    print('allnow, ', end='')

    for key in info_dic[mdid].keys():
        if key == 'ssid':
            continue
        print(str(key) + ', ', end='')

    for item in info_dic['part']:
        for key in info_dic['part'][item].keys():
            if key == 'aid':
                continue
            if key == 'view':
                print('view_' + item + ', ', end='')
            else:
                print(str(key) + ', ', end='')

    print('')   # 换一行

    #   输出数据
    print(str(len(info_dic['part'])) + ', ', end='')

    for key, value in info_dic[mdid].items():
        if key == 'ssid':
            continue
        if key == 'title':
            print(str(mdid) + ', ', end='')
        else:
            print(str(value) + ', ', end='')

    for key in info_dic['part'].keys():
        for k in info_dic['part'][key]:
            if k == 'aid':
                continue
            print(str(info_dic['part'][key][k]) + ', ', end='')

    print('\n')  # 换两行

    sys.stdout = origin
    f.close()   # 归还输出流，关闭文件


def final_main():
    md_list = [
        28228266, 28228168, 28228368, 28228265, 28228332, 28228304, 28228339, 28228355, 28228394, 28228269,
        28228414, 28228440, 28228439, 28228443, 28228438, 28228433, 28228413, 28228276, 28228462, 28228410,
        28228434, 28228277, 28228448, 28228386, 28228409, 28228420, 28228367, 28228406, 28228449, 28228437,
        28228268, 28228119]
    name, path = filename_according_time()  # 获取文件名称及路径
    # 开始创建该文件，若文件已存在则删除重新创建
    if os.path.exists(path):
        os.remove(path)
    for i in md_list:
        flag = True
        while flag:
            try:
                res = get_from_md(i)
                write_chart(i, res, path)
                print('{0:<70}'.format(res[i]['title']) + '\tOK!')
                flag = False
            except Exception as e:
                print(e)
                time.sleep(1)
        time.sleep(1)
    # 创建成功后发送该邮件
    # emailSender.send_email_appendix(name, path)
    print(name + '____数据已经全部完毕____')


final_main()
