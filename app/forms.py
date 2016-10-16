from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, PasswordField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


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


class AddTransactionForm(FlaskForm):
    from datetime import datetime
    title = StringField('name', validators=[DataRequired(),Length(1,120)])
    date = DateField('date', default=datetime.today, validators=[DataRequired()])
    cost = DecimalField('cost', validators=[DataRequired(),NumberRange(0)])
    category = SelectField(coerce=int, label='Category', validators=[DataRequired()])

class AddCategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(),Length(1,120)])

