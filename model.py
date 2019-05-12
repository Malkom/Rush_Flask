#!/usr/bin/env python3

from werkzeug.security import check_password_hash
from flask import session, flash


def create_user(db, username, email, hash_password):
    db.execute(
        'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
        (username, email, hash_password))
    db.commit()


def login(db, email, password):
    error = None

    user = db.execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    ).fetchone()

    if user is None:
        error = 'Email inconnu'
    elif not check_password_hash(user['password'], password):
        error = 'Password erroné'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
    else:
        flash(error)


def get_users(db):
    users = db.execute(
        'SELECT * FROM users'
    ).fetchall()
    return users


def delete(db, id):
    db.execute(
        'DELETE FROM users WHERE id = ?', (id,)
    )
    db.commit()


def show_user(db, user_id):
    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    return user
