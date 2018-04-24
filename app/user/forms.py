#-*- coding:utf-8 -*
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField
class LoginForm(Form):
    user_name = StringField('username',validators=[Required()])
    password = PasswordField('password',validators=[Required()])
    submit = SubmitField('登陆')
    