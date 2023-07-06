import pyodbc
import click
from flask import current_app, g

def get_connection_string():
    server='LP-5CD2079WQ5\SQLEXPRESS'
    username='admin1'
    password='yb3OZAYgNztWA+mtCFL'
    database='PythonReact'

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return connection_string

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        try:
            cursor = db.cursor()
            cursor.execute(f.read().decode('utf8'))
            db.commit()
        except pyodbc.Error as error:
            print(str(error))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pyodbc.connect(get_connection_string())
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()