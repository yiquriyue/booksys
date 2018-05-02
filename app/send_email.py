#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr
from flask_mail import Message 
from flask import request,render_template

my_sender='1341799937@qq.com'    # 发件人邮箱账号
my_pass = 'kjcazhzusclljdcb'              # 发件人邮箱密码

def send_email(to,subject,template,**kwargs):
    try:
        try:
            mail_msg =render_template(template+'.txt',**kwargs)
        except:
            mail_msg =kwargs['postcode']
        msg=MIMEText(mail_msg,'plain','utf-8')
        msg['From']=formataddr(["FromBookShop",my_sender]) 
        msg['To']=formataddr(["FK",to])
        msg['Subject']=subject
        #msg.body = "helloworld"
        print msg
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass) 
        server.sendmail(my_sender,[to,],msg.as_string())
        server.quit()
        print "成功发送邮件" 
    except BaseException,e:
        print "失败发送邮件" 
        print e
        
        
        
        
        
        
        
       
       