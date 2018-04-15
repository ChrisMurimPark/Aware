from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# define app
app = Flask(__name__)
app.config.from_object('config')

# define database
db = SQLAlchemy(app)

# define login manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = ''

# define mailer
mail = Mail(app)

from app import views, models

