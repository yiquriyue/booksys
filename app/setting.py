# _*_ coding: utf-8 _*_
import os
#调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True
#session必须要设置key
SECRET_KEY='59_^13$$*&61%2_+6+8$%^&/*'

#mysql数据库连接信息,这里改为自己的账号
#SQLALCHEMY_DATABASE_URI = "mysql://root:original123@172.31.50.197:3306/test?charset=utf8"
SQLALCHEMY_DATABASE_URI = "mysql://root://////@localhost:3306/test?charset=utf8"


UPLOAD_FOLDER = os.path.join(os.getcwd(),'app','static','files')
QRCODE_FOLDER = os.path.join(os.getcwd(),'app','static','qrcode')

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

URL_LIST = ['/user','/book']

# FLASK_MAIL_SUBJECT_PREFIX ='kjcazhzusclljdcb' 

# FLASK_MAIL_SENDER ="1341799937@qq.com"

# MAIL_SERVER = 'smtp.qq.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = True
# MAIL_USERNAME = '1341799937@qq.com'
# MAIL_PASSWORD = 'kjcazhzusclljdcb'
