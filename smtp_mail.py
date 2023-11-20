#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class SendSmtpMail(object):
    # def __int__(self):

    def mail(self, concattext, subjecttext):
        my_sender = '1624231060@qq.com'  # 发件人邮箱账号
        my_pass = 'tdnqtojuzskiccig'  # 发件人邮箱密码
        my_user = 'ririyeye_wx@qq.com'  # 收件人邮箱账号，我这边发送给自己
        ret = True
        try:
            msg = MIMEText(concattext, 'plain', 'utf-8')
            msg['From'] = formataddr(["mm_pc", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["pixel4", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = subjecttext  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        if ret:
            print("邮件发送成功")
        else:
            print("邮件发送失败")
        return ret


