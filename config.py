import os

# WTForms
WTF_CSRF_ENABLED = True
SECRET_KEY = '20xx-hack-pack'
SECURITY_PASSWORD_SALT = 'email-for-good-time'

# SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

#mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = 'awarepersonalfinance@gmail.com'
MAIL_PASSWORD = 'too_aware_for_me'

# mail accounts
MAIL_DEFAULT_SENDER = 'awarepersonalfinance@gmail.com'
