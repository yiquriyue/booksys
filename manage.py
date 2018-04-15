#-*- coding:utf-8 -*-
from app import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.models import db

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def db_create():
	try:
		db.create_all()
		print "database create success"
	except BaseException,e:
		print e

@manager.command
def db_drop():
	db.drop_all()
	#delpassdb()

#@manager.command
if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0', port=80)
	except BaseException,e:
		print e
