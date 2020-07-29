from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flaskblog.config import Config

from flask_misaka import Misaka
from flask_pagedown import PageDown

db = SQLAlchemy()
admin = Admin(name='Mercatelli', template_mode='bootstrap3')
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()
pagedown = PageDown()
md = Misaka()

def create_app(config_class=Config):

	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	md.init_app(app)
	pagedown.init_app(app)

	from flaskblog.models import MyAdminIndexView
	admin.init_app(app,index_view=MyAdminIndexView())
	admin.add_link(MenuLink(name='Home', url='/'))
	admin.add_link(MenuLink(name='Logout', url='/logout'))

	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts

	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)


	return app
