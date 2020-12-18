# -*- coding: utf-8 -*-

from lxml import etree

with open('pages.html', 'r') as f:
    html = f.read()
    et = etree.HTML(html)
    fin = et.xpath("//span[@style='color:red;']/text()")
    for i in range(len(fin)):
        if i > 13 and i % 2 == 1:
            print(str(fin[i].replace('\xa0', '')))
