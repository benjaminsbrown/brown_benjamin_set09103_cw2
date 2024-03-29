# coding: utf-8
from flask import Flask, render_template, url_for, request, redirect, session, flash, g, abort
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from  contextlib  import  closing

import sqlite3

app = Flask(__name__)
app.secret_key = '\xf1yW\xafT\xf5\x11o\xb4\xd5a\x98\xf12-\xd3`\x99\xe6m\x01\t\xae\x83'
app.database = "sample.db"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def init_db():
    with  closing(connect_db()) as db:
        with  app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'Logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login ya snake!')
            return redirect(url_for('login'))
    return wrap

@app.route('/login', methods=['GET', 'POST'])
def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'ben' or request.form['password'] != 'brown':
                error = 'Invalid Username and/or Password please try again.'
            else:
                session['Logged_in'] = True
                flash('Logged in')
                return redirect(url_for('root'))
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
        session.pop('Logged_in', None)
        flash('Logged out')
        return redirect(url_for('login'))

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/')
@login_required
def root():
	    return render_template('home.html'), 200

@app.route('/home')
@login_required
def show_entries():
    g.db = connect_db()
    cur = g.db.execute('SELECT title, text from entries order by id desc')
    entries = [dict(title = row[0], text=row[1]) for row in cur.fetchall()]
    return  render_template ('show_entries.html', entries=entries)

@app.route('/signup')
def signup():
    return render_template('signup.html'), 200

@app.route('/add', methods=['POST'])
def add_entry():
    g.db.execute("INSERT INTO entries (title,text) VALUES (?,?)",[ request . form [ 'title' ],  request . form [ 'text' ]])
    g.db.commit()
    flash ('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/demigods/')
@login_required
def demigods():
	return render_template('demigods.html'), 200

@app.route('/demigods.html')
@login_required
def demigodshtml():
	return render_template('demigods.html'), 200

@app.route('/greeks/')
@login_required
def greeks():
	return render_template('greeks.html'), 200

@app.route('/greeks.html')
@login_required
def greekshtml():
	return render_template('greeks.html'), 200

@app.route('/greeks/greekgods.html')
@login_required
def greekgods():
	return render_template('greekgods.html'), 200

@app.route('/greeks/greekgods/zues.html')
@login_required
def zues():
	return render_template('zues.html'), 200
@app.route('/greeks/greekgods/hera.html')
@login_required
def hera():
	return render_template('hera.html'), 200
@app.route('/greeks/greekgods/ares.html')
@login_required
def ares():
	return render_template('ares.html'), 200
@app.route('/pantheon.html')
@login_required
def pantheonshtml():
	return render_template('pantheon.html'), 200
@app.route('/greeks/pantheon/')
@login_required
def pantheon():
	return render_template('pantheon.html'), 200
@app.route('/romans/')
@login_required
def romans():
	return render_template('romans.html'), 200
@app.route('/romans.html')
@login_required
def romanshtml():
	return render_template('romans.html'), 200

@app.route('/romans/romansgods.html')
@login_required
def romangods():
	return render_template('romangods.html'), 200

@app.route('/romans/romansgods/jupiter.html')
@login_required
def jupiter():
	return render_template('jupiter.html'), 200

@app.route('/romans/romansgods/juno.html')
@login_required
def juno():
	return render_template('juno.html'), 200

@app.route('/romans/romansgods/mars.html')
@login_required
def mars():
	return render_template('mars.html'), 200
@app.errorhandler(404)
def page_not_found(error):
	return render_template("youfool.html"), 404

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
