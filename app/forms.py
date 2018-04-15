from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, PasswordField, SelectField, DecimalField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Required


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email(),Length(7,120)])
    password = PasswordField('password', validators=[DataRequired(),Length(4,64)])


class RegisterForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired(),Length(1,64)])
    last_name = StringField('last_name', validators=[DataRequired(),Length(1,64)])
    email = StringField('email', validators=[DataRequired(),Email(),Length(7,120)])
    password = PasswordField('password', validators=[DataRequired(),Length(4,64)])
    password_confirm = PasswordField('password_confirm',
            validators=[DataRequired(),EqualTo('password', message='Passwords do not match')])


class AddTransactionSingleForm(FlaskForm):
    from datetime import datetime
    title = StringField('name', validators=[DataRequired(),Length(1,120)])
    date = DateField('date', default=datetime.today, validators=[DataRequired()])
    cost = DecimalField('cost', validators=[DataRequired(),NumberRange(0)])
    category = SelectField('category', coerce=int, validators=[DataRequired()])

class AddTransactionOverTimeForm(FlaskForm):
    from datetime import datetime
    title = StringField('name', validators=[DataRequired(),Length(1,120)])
    date = DateField('date', default=datetime.today, validators=[DataRequired()])
    cost = DecimalField('cost', validators=[DataRequired(),NumberRange(0)])
    category = SelectField('category', coerce=int, validators=[DataRequired()])
    frequency = SelectField('frequency', coerce=int, validators=[DataRequired()])
    occurrences = IntegerField('occurrences', validators=[DataRequired(),NumberRange(2)])


class AddCategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(),Length(1,120)])


class StartEndDateForm(FlaskForm):
    # no validators are required for these fields because there is a default
    # value used if none is provided
    from .aware_utils import first_day_current_month, last_day_current_month
    start = DateField('start', default=first_day_current_month())
    end = DateField('end', default=last_day_current_month())

