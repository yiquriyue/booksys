#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr
from flask_mail import Message 
from flask import request,render_template
from . import mail
from . import app
my_sender='1341799937@qq.com'    # 发件人邮箱账号
my_pass = 'kjcazhzusclljdcb'              # 发件人邮箱密码

def send_email(to,subject,template,**kwargs):
    try:
        # print to,subject,template
        # print kwargs
        # msg = Message('[bookShop]'+subject,sender='admin<1341799937@qq.com>',recipients=[to],charset='utf-8')
        # print "0000000000000000000"
        #print render_template(template+'.txt',**kwargs)
        #msg.body = render_template(template+'.txt',**kwargs).decode('utf8')
        #msg.html = render_template(template+'.html',**kwargs)
        # with open(os.path.join(os.path.dirname(),template,user,confirm.txt)) as f:
            # s=f.read()
        mail_msg =render_template(template+'.txt',**kwargs)
        msg=MIMEText(mail_msg,'plain','utf-8')
        msg['From']=formataddr(["FromBookShop",my_sender]) 
        msg['To']=formataddr(["FK",to])
        msg['Subject']=subject
        #msg.body = "helloworld"
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass) 
        server.sendmail(my_sender,[to,],msg.as_string())
        server.quit()
        print "成功发送邮件" 
    except BaseException,e:
        print "失败发送邮件" 
        print e
        
        
        
        
        
        
        
       
       