#In ubuntu use 'nano .bashrc' to create Environments Variables:

#export SECRET_KEY='your_secret_key'
#export SQLALCHEMY_DATABASE_URI='your_path_folder'

#export EMAIL_USER='your_user_email@gmail.com'
#export EMAIL_PASSWORD='your_app_password'

#Save file and restart terminal
#For safety reasons it's necessary create an App Password in your Google Account


import os

class Config:

	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

	EMAIL_ADMIN = os.environ.get('EMAIL_ADMIN')
