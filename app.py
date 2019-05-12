#!/usr/bin/env python3
from json import dump

from controller import *
from db import get_db
import os
from flask import Flask, request, session, g, redirect, url_for, render_template


app = Flask(__name__)  # that means that your app name will be the same as the file

app.config.from_object(__name__)  # load config from this file, app.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)


@app.route('/')  # Route for index
def index():
    return render_template('base.html')


@app.route('/register', methods=('GET', 'POST'))  # Route for register form
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        register_controller(db, username, email, password, confirm_password)
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_controller(db, email, password)
        return redirect(url_for('index'))

    return render_template('login.html')


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/users', methods=('GET', 'POST', 'DELETE'))
def crud():
    db = get_db()

    if request.method == 'GET':
        users = getusers_controller(db)
        return render_template('users.html', users=users)

    if request.method == 'DELETE':
        user_id = request.args.get('user_id')
        delete_controller(db, user_id)
        users = getusers_controller(db)
        return render_template('users.html', users=users)

    if request.method == 'POST':
        user_id = request.args['user_id']
        user = show_controller(db, user_id)
        return render_template('show.html', user=user)



    """if user_id is not None:"""



if __name__ == "__main__":
    app.run(debug=True)

