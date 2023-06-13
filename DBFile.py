import flask as fl
import sqlite3
import os

DATABASE = '/tmp/shopData.db'
DEBUG = True
SECRET_KEY = 'ADKdafkq301g2kvka;kf023'

app = fl.Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path,'shopData.db')))

def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(fl.g ,'link_db'):
        fl.g.link_db = connect_db()
    return fl.g.link_db



