from app import app, lm, db
from flask import render_template, redirect, flash, g, request, url_for
from .forms import LoginForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
import bcrypt


@app.route('/')
@app.route('/index')
@login_required
def index():
    flash("Hello, {}".format(g.user.first_name))
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET','POST'])
def login():
    # check if user is already logged in
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email_match = User.query.filter(User.email == form.email.data)
        if email_match.count() != 1:
            flash("Sorry, there is no user with that email.")
            return redirect(url_for('login'))
        user = email_match.all()[0]
        if not user.verify_password(form.password.data): 
            flash("Sorry, the password you entered is not correct.")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                last_name=form.last_name.data, 
                email=form.email.data,
                password=form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Thanks for registering!')
        except IntegrityError:
            db.session.rollback()
            flash('That email is already registered.')
            return redirect(url_for('register'))
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


# sets a global field to track lm's current_user before each request
@app.before_request
def before_request():
    g.user = current_user


# used by lm to log user in upon success
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


