#!/usr/bin/env python3


from model import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash


def register_controller(db, username, email, password, confirm_password):
    error = None

    if not username:
        error = 'Le pseudo est obligatoire'
    elif not password:
        error = 'Le mot de passe est obligatoire'
    elif not email:
        error = "L'email est obligatoire"
    elif password != confirm_password:
        error = "Les mots de passe doivent être équivalent"

    if error is None:
        hash_password = generate_password_hash(password)
        create_user(db, username, email, hash_password)
    else:
        flash(error)


def login_controller(db, email, password):
    login(db, email, password)


def getusers_controller(db):
    users = get_users(db)
    return users


def delete_controller(db, id):
    delete(db, id)


def show_controller(db, user_id):
    user = show_user(db, user_id)
    return user

