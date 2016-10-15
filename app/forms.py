from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email(),Length(7,120)])
    password = PasswordField('password', validators=[DataRequired(),Length(4,64)])


class RegisterForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired(),Length(1,64)])
    last_name = StringField('last_name', validators=[DataRequired(),Length(1,64)])
    email = StringField('email', validators=[DataRequired(),Length(7,120)])
    password = PasswordField('password', validators=[DataRequired(),Length(4,64)])
    password_confirm = PasswordField('password_confirm',
            validators=[DataRequired(),EqualTo('password', message='Passwords do not match')])

