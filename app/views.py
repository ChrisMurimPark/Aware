from app import app, lm, db
from flask import render_template, redirect, flash, g, request, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from .forms import LoginForm, RegisterForm, AddTransactionSingleForm, AddTransactionOverTimeForm, AddCategoryForm, StartEndDateForm
from .models import User, Transaction, Category
from .analytics import get_spending_by_category, get_total_spending
from .aware_utils import first_day_current_month, last_day_current_month, commit_db
from .nocache import nocache

import bcrypt
import re
from datetime import timedelta
from dateutil.relativedelta import relativedelta


@app.route('/')
@app.route('/index')
@login_required
@nocache
def index():
    flash('Hello, {}.'.format(g.user.first_name))
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET','POST'])
def login():
    if user_set():
        return redirect(url_for('index'))
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', title='Login', form=form)
    user = User.query.filter(User.email == form.email.data).first()
    if user is None:
        flash('Sorry, there is no user with that email.')
        return redirect(url_for('login'))
    if not user.verify_password(form.password.data): 
        flash('Sorry, the password you entered is not correct.')
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if user_set():
        return redirect(url_for('index'))
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template('register.html', title='Register', form=form)
    user = User(first_name=form.first_name.data,
            last_name=form.last_name.data, 
            email=form.email.data,
            password=form.password.data,
            confirmed=False)
    db.session.add(user)
    if not commit_db(db.session):
        flash('Sorry, something went wrong during registration.')
        return redirect(url_for('register'))
    login_user(user)
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
@nocache
def profile():
    if not user_set():
        return redirect(url_for('index'))
    return render_template('profile.html', title='Profile')

    
@app.route('/transactions')
@login_required
@nocache
def transactions():
    transactions = g.user.transactions.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=transactions, title='Transactions')


@app.route('/add_transaction')
@login_required
@nocache
def add_transaction():
    return render_template('add_transaction.html', title='Transactions')


@app.route('/add_transaction/over_time', methods=['GET', 'POST'])
@login_required
@nocache
def add_transaction_over_time():
    form = AddTransactionOverTimeForm()
    form.category.choices = [(c.id, c.name) for c in g.user.categories.order_by(Category.name).all()]
    form.frequency.choices = [(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')]
    if not form.validate_on_submit():
        return render_template('add_transaction_over_time.html', title='Transactions', form=form)
    category = Category.query.get(form.category.data)
    name = form.title.data
    date = form.date.data
    cost = form.cost.data
    freq = form.frequency.data
    occurrences = form.occurrences.data
    time = timedelta(1)
    if freq is 2:
        time = timedelta(weeks=1)
    elif freq is 3:
        time = relativedelta(months=+1)
    for i in range(occurrences):
        t = Transaction(name=name, date=date, category=category, cost=cost/occurrences, user=g.user)
        db.session.add(t)
        date += time
    if not commit_db(db.session):
        flash('Sorry, something went wrong while creating the transaction.')
        return redirect(url_for('index'))
    return redirect(url_for('add_transaction_result'))


@app.route('/add_transaction/single', methods=['GET', 'POST'])
@login_required
@nocache
def add_transaction_single():
    form = AddTransactionSingleForm()
    form.category.choices = [(c.id, c.name) for c in g.user.categories.order_by(Category.name).all()]
    if not form.validate_on_submit():
        return render_template('add_transaction_single.html', title='Transactions', form=form)
    category = Category.query.get(form.category.data)
    name = form.title.data
    date = form.date.data
    cost = form.cost.data
    t = Transaction(name=name, date=date, category=category, cost=cost, user=g.user)
    db.session.add(t)
    if not commit_db(db.session):
        flash('Sorry, something went wrong while creating the transaction.')
        return redirect(url_for('index'))
    return redirect(url_for('add_transaction_result'))


@app.route('/add_transaction/result')
@login_required
@nocache
def add_transaction_result():
    return render_template('add_transaction_result.html', title='Transactions', result='Success!')

@app.route('/delete_transactions', methods=['GET', 'POST'])
@login_required
@nocache
def delete_transaction():
    data = request.args.get('data')
    pattern = re.compile('[0-9]+')
    ids = pattern.findall(data)
    for d in ids:
        if d is not -1:
            transaction = Transaction.query.filter(Transaction.id == d).first() 
            db.session.delete(transaction)
    if not commit_db(db.session):
        flash('Sorry, Something went wrong while deleting the transaction(s).')
        return jsonify(result='Sorry!')
    flash('Successfully deleted transaction(s).')
    return jsonify('Success!')


@app.route('/categories')
@login_required
@nocache
def categories():
    categories = g.user.categories.order_by(Category.name).all()
    return render_template('categories.html', categories=categories, title='Categories')


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
@nocache
def add_category():
    form = AddCategoryForm()
    if not form.validate_on_submit():
        return render_template('add_category.html', title='Categories', form=form)
    db.session.add(Category(name=form.name.data, user=g.user))
    if not commit_db(db.session):
        flash('Sorry, something went wrong while creating the transaction.')
        return redirect(url_for('index'))
    return redirect(url_for('categories'))


@app.route('/analytics', methods=['GET','POST'])
@login_required
@nocache
def analytics():
    form = StartEndDateForm()
    start = first_day_current_month()
    end = last_day_current_month()
    if form.validate_on_submit():
        start = form.start.data
        end = form.end.data
    category_data = get_spending_by_category(start, end)
    total_cost_pretty = '$0.00'
    total_cost = get_total_spending(start, end)
    if total_cost is not None:
        total_cost_pretty = '${:,.2f}'.format(total_cost)
    return render_template('analytics.html', title='Analytics', form=form, by_category=category_data, total=total_cost_pretty)

   
# sets a global field to track lm's current_user before each request
@app.before_request
def before_request():
    g.user = current_user


# used by lm to log user in upon success
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# returns whether user is logged in
def user_set():
    if g.user is None or not g.user.is_authenticated:
        return False
    return True

