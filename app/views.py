from app import app, lm, db
from flask import render_template, redirect, flash, g, request, url_for, jsonify
from .forms import LoginForm, RegisterForm, AddTransactionSingleForm, AddTransactionOverTimeForm, AddCategoryForm, StartEndDateForm
from .models import User, Transaction, Category
from .analytics import get_spending_by_category, get_total_spending
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from .nocache import nocache
import bcrypt
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@app.route('/')
@app.route('/index')
@login_required
@nocache
def index():
    flash("Hello, {}.".format(g.user.first_name))
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
    transactions = g.user.transactions.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=transactions, title='Transactions')


@app.route('/add_transaction')
@login_required
@nocache
def add_transaction():
    if not user_set():
        return redirect(url_for('index'))
    return render_template('add_transaction.html', title='Transactions')


@app.route('/add_transaction/over_time', methods=['GET', 'POST'])
@login_required
@nocache
def add_transaction_over_time():
    if not user_set():
        return redirect(url_for('index'))
    form = AddTransactionOverTimeForm()
    form.category.choices = [(c.id, c.name) for c in g.user.categories.all()]
    form.frequency.choices = [(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')]
    if form.validate_on_submit():
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
        try:
            db.session.commit()
        except IntegrityError:
            flash("Something went wrong while creating the transaction.")
            return redirect(url_for('index'))
        return redirect(url_for('add_transaction_result'))
    return render_template('add_transaction_over_time.html', title='Transactions', form=form)


@app.route('/add_transaction/single', methods=['GET', 'POST'])
@login_required
@nocache
def add_transaction_single():
    if not user_set():
        return redirect(url_for('index'))
    form = AddTransactionSingleForm()
    form.category.choices = [(c.id, c.name) for c in g.user.categories.all()]
    if form.validate_on_submit():
        category = Category.query.get(form.category.data)
        name = form.title.data
        date = form.date.data
        cost = form.cost.data
        t = Transaction(name=name, date=date, category=category, cost=cost, user=g.user)
        db.session.add(t)
        try:
            db.session.commit()
        except IntegrityError:
            flash("Something went wrong while creating the transaction.")
            return redirect(url_for('index'))
        return redirect(url_for('add_transaction_result'))
    return render_template('add_transaction_single.html', title='Transactions', form=form)


@app.route('/add_transaction/result')
@login_required
@nocache
def add_transaction_result():
    if not user_set():
        return redirect(url_for('index'))
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
    try:
        db.session.commit()
    except IntegrityError:
        flash("Sorry! Something went wrong while deleting the transaction(s).")
        return jsonify(result="Sorry!")
    flash("Successfully deleted transaction(s).")
    return jsonify("Success!")


@app.route('/categories')
@login_required
@nocache
def categories():
    if not user_set():
        return redirect(url_for('index'))
    categories = g.user.categories.order_by(Category.name).all()
    return render_template('categories.html', categories=categories, title='Categories')


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
@nocache
def add_category():
    if not user_set():
        return redirect(url_for('index'))
    form = AddCategoryForm()
    if form.validate_on_submit():
        db.session.add(Category(name=form.name.data, user=g.user))
        try:
            db.session.commit()
        except IntegrityError:
            flash("Something went wrong while creating the transaction.")
            return redirect(url_for('index'))
        return redirect(url_for('categories'))
    return render_template('add_category.html', title='Categories', form=form)


@app.route('/analytics', methods=['GET','POST'])
@login_required
@nocache
def analytics():
    if not user_set():
        return redirect(url_for('index'))
    form = StartEndDateForm()
    start = datetime.today() - timedelta(weeks=1)
    end = datetime.today()
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


# ensures g.user is set correctly. this should only return false during special circumstances
def user_set():
    if g.user is None or not g.user.is_authenticated:
        # log here
        flash('Something went wrong')
        return False
    return True

