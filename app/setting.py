# _*_ coding: utf-8 _*_

#调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True
#session必须要设置key
SECRET_KEY='59_^13$$*&61%2_+6+8$%^&/*'

#mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://root://////@localhost:3306/test"

URL_LIST = ['/user']
