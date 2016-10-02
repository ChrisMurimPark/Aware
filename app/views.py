from app import app
from flask import render_template, redirect, flash
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Email: {}, Password: {}'.format(form.email.data,
            form.password.data))
        return redirect('/index')
    return render_template('login.html', title='Login', form=form)

