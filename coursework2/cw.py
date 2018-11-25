from flask import Flask, render_template, url_for, request, redirect, session, flash, g

from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
# import sqlite3

app = Flask(__name__)
app.secret_key = '\xf1yW\xafT\xf5\x11o\xb4\xd5a\x98\xf12-\xd3`\x99\xe6m\x01\t\xae\x83'
app.database = "sample.db"

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
                return redirect(url_for('home'))
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
        session.pop('Logged_in', None)
        flash('Logged out')
        return redirect(url_for('home'))

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/')
@login_required
def root():
	    return render_template('home.html'), 200
@app.route('/home')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('home.html', posts=posts), 200

@app.route('/signup')
def signup():
    return render_template('signup.html'), 200
@app.route('/greeks/')
def greeks():
    return render_template('greeks.html'), 200

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
