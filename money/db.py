import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
  if 'db' not in g:
    g.db = sqlite3.connect(
      current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
    g.db.execute("PRAGMA foreign_keys = 1")
    g.db.commit()
  return g.db


def close_db(e=None):
  db = g.pop('db', None)
  if db is not None:
    db.close()


def init_db():
  db = get_db()
  with current_app.open_resource('schema.sql') as f:    # opens file relative to money package
    db.executescript(f.read().decode('utf8'))


# creates cli command called init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
  init_db()
  click.echo('Initialized the database.')


def init_app(app):
  app.teardown_appcontext(close_db)     # call this function when cleaning up after response is returned
  app.cli.add_command(init_db_command)  # adds new command that can be called with flask command