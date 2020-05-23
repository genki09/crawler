# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time

smtpserver = 'smtp.163.com'
smtpport = 465
sender = '15029336688@163.com'
sender_pwd = '7758521abcd'
rece = 'haoyang_wei@163.com'
# rece = '986084267@qq.com'
mail_username = ''


def send_email_appendix(filename, fileway):
    message = MIMEMultipart()

    mail_title = '今日数据：' + filename
    mail_inside = MIMEText('今日もよろしくお願いします！！', 'plain', 'UTF-8')

    message['From'] = sender
    message['To'] = rece
    message['Subject'] = Header(mail_title, 'UTF-8')
    message.attach(mail_inside)

    attr = MIMEText(open(fileway, 'rb').read(), 'base64', 'UTF-8')
    attr["Content-Type"] = 'application/octet-stream'
    attr["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
    message.attach(attr)

    smtpobj = smtplib.SMTP_SSL(smtpserver, port=smtpport)
    smtpobj.login(sender, sender_pwd)
    smtpobj.sendmail(sender, rece, message.as_string())
    print('\n邮件发送成功！')
    smtpobj.quit()


def test_text_time():
    message = MIMEMultipart()

    mail_title = '测试：{}'.format(str(time.strftime('%m-%d %H$%M$%S', time.localtime(time.time()))))
    mail_inside = MIMEText('ます！！', 'plain', 'UTF-8')

    message['From'] = sender
    message['To'] = 'haoyang_wei@163.com'
    message['Subject'] = Header(mail_title, 'UTF-8')
    message.attach(mail_inside)

    smtpobj = smtplib.SMTP_SSL(smtpserver, port=smtpport)
    smtpobj.login(sender, sender_pwd)
    smtpobj.sendmail(sender, '986084267@qq.com', message.as_string())
    print('\n邮件发送成功！')
    smtpobj.quit()

