from flask_app import app
from flask_app import bcrypt
from flask_app.models.user import User
from flask import flash, redirect, render_template, request, session, url_for


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/users/register')
def register_form():
    return render_template('register_form.html')


@app.post('/users/register')
def register_user():
    if not User.registration_is_valid(request.form):
        return redirect(url_for('register_form'))

    user = User.find_user_by_email(request.form['email'])
    if user:
        flash('Email in use. Please login.', 'auth')
        return redirect(url_for('login_form'))

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
    }

    user_id = User.register_user(data)
    session['user_id'] = user_id

    return redirect(url_for('wall'))


@app.get('/users/login')
def login_form():
    return render_template('login_form.html')


@app.post('/users/login')
def login_user():
    if not User.login_is_valid(request.form):
        return redirect(url_for('login_form'))

    user = User.find_user_by_email(request.form['email'])
    if not user:
        flash('Invalid credentials.', 'auth')
        return redirect(url_for('login_form'))

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid credentials.', 'auth')
        return redirect(url_for('login_form'))

    session['user_id'] = user.id
    return redirect(url_for('wall'))


@app.post('/users/logout')
def logout_user():
    session.clear()
    return redirect(url_for('index'))
