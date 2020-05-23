# -*- coding:utf-8 -*-

import datetime
import time
import emailSender


def koko():
    while True:
        while True:
            now = datetime.datetime.now()
            allow = [0, 8, 16]
            if now.hour in allow:
                break
            time.sleep(3)    # 每过3秒检测一次

        emailSender.test_text_time()

        time.sleep(3600)    # 一旦检测成功，下一次检测会在一个小时后


koko()
