# -*- coding:utf-8 -*-

import datetime
import time
import bangumi


def koko():
    while True:
        while True:
            now = datetime.datetime.now()
            allow = [15, 18, 21]
            if now.hour in allow:
                break
            time.sleep(2)    # 每过2秒检测一次

        bangumi.final_main()

        time.sleep(3600)    # 一旦检测成功，下一次检测会在一个小时后


# koko()
print(datetime.datetime.now())
