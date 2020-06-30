from datetime import datetime
from flask import current_app, redirect, url_for
from flaskblog import db, bcrypt, login_manager, admin
from flask_login import UserMixin, current_user, logout_user, login_required
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog.config import Config


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	post = db.relationship('Post', backref='author', lazy=True)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __unicode__(self):
		return self.username

	def get_reset_token(self, expires_sec=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"



class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_active and (current_user.email == 'admin@cu.com')

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('users.login'))


class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_active and (current_user.email == 'admin@cu.com')

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('users.login'))

class MyUserModelView(MyModelView):
	column_exclude_list = []
	column_display_pk = True
	can_create = True
	can_edit = True
	can_delete = True
	create_modal = True

admin.add_view(MyUserModelView(User, db.session))
admin.add_view(MyUserModelView(Post, db.session))

'''
		return current_user.is_authenticated and current_user.is_active and value
		if environ.get('EMAIL_ADMIN'):
		if (current_user.email == 'admin@cu.com'):
		if current_app.config['EMAIL_ADMIN']:
			return current_user.is_authenticated and current_user.is_active
			return current_user.is_authenticated and current_user.is_active and (current_user.email == 'admin@cu.com')
			s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
'''
