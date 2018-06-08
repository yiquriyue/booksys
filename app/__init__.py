#-*- coding:utf-8 -*-
from flask import Flask,render_template,redirect,url_for
from flask_mail import Mail
from werkzeug.routing import BaseConverter
from setting import URL_LIST
from flask_login import LoginManager

class RegexConverter(BaseConverter):
    def __init__(self,map,*arge):
        self.map = map
        self.regex = args[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config.from_object('app.setting')
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)
mail= Mail(app)

def general():
    #return render_template('user_index.html')
    return redirect(url_for('home'))

url_list = URL_LIST
for url in url_list:
    app.add_url_rule(url, 'general', general)
# 添加蓝本
from user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/api')
from home import home as home_blueprint
app.register_blueprint(home_blueprint, url_prefix='/api')
from book import book as book_blueprint
app.register_blueprint(book_blueprint, url_prefix='/api')
from manager import manager as manager_blueprint
app.register_blueprint(manager_blueprint, url_prefix='/api')
from activity import activity as activity_blueprint
app.register_blueprint(activity_blueprint, url_prefix='/api')
from order import order as order_blueprint
app.register_blueprint(order_blueprint, url_prefix='/api')
