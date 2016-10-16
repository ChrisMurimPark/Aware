from app import app, lm, db
from flask import render_template, redirect, flash, g, request, url_for
from .forms import LoginForm, RegisterForm, AddTransactionForm
from .models import User, Transaction, Category
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from .nocache import nocache
import bcrypt
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
@nocache
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
        user = User.query.filter(User.email == form.email.data).first()
        if user is None:
            flash("Sorry, there is no user with that email.")
            return redirect(url_for('login'))
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
    return redirect(url_for('index'))


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
            login_user(user)
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash('That email is already registered.')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/profile')
@login_required
@nocache
def profile():
    if g.user is None or not g.user.is_authenticated:
        # send an email here?
        flash('Something went wrong')
        return redirect(url_for('index'))
    return render_template('profile.html', title='Profile')

    
@app.route('/transactions')
@login_required
@nocache
def transactions():
    if not user_set():
        return redirect(url_for('index'))
    # transactions = [{'name': 'Aldi', 'date': '2016-01-01', 'category': 'Groceries', 'cost': '18.43'},{'name': 'Emerald City Coffee', 'date': '2016-01-02', 'category': 'Coffee Shop', 'cost': '2.80'}]
    transactions = g.user.transactions.all()
    return render_template('transactions.html', transactions=transactions, title='Transactions')


@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
@nocache
def add_transaction():
    if not user_set():
        return redirect(url_for('index'))
    form = AddTransactionForm()
    if form.validate_on_submit():
        # TODO clean up and replace hard coded category and date
        category = Category(name='Groceries', user=g.user)
        name = form.title.data
        date = datetime.now()
        cost = form.cost.data
        t = Transaction(name=name, date=date, category=category, cost=cost, user=g.user)
        db.session.add(t)
        try:
            db.session.commit()
        except IntegrityError:
            flash("Something went wrong while creating the transaction.")
            redirect(url_for('index'))
    return render_template('add_transaction.html', title='New Transaction', form=form)


# sets a global field to track lm's current_user before each request
@app.before_request
def before_request():
    g.user = current_user


# used by lm to log user in upon success
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# ensures g.user is set correctly. this should only return false during special circumstances
def user_set():
    if g.user is None or not g.user.is_authenticated:
        # send an email here?
        flash('Something went wrong')
        return False
    return True

