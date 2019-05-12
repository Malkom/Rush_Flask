#!/usr/bin/env python3

import sqlite3
import click
from flask import Flask, current_app, g

app = Flask(__name__)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
        current application context.
        """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


@app.cli.command('initdb')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@app.teardown_request
def close_db(e=None):
    db = g.pop('DATABASE', None)
    if db is not None:
        db.close()


def query_db(query):
    db = get_db()
    query = db.execute(query)
    db.commit()
    query.fetchall()
    close_db()
