from flask import Flask, render_template, url_for, request, redirect, session, flash
from functools import wraps
app = Flask(__name__)
app.secret_key = "super secret"

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
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Username and/or Password please try again.'
            else:
                session['Logged_in'] = True
                flash('You were just logged in!')
                return redirect(url_for('home'))
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
        session.pop('Logged_in', None)
        flash('You were just logged out!')
        return redirect(url_for('home'))

@app.route('/')
@login_required
def home():
	    return render_template('home.html'), 200
@app.route('/signup')
def signup():
	    return render_template('signup.html'), 200
@app.route('/greeks/')
def greeks():
	    return render_template('greeks.html'), 200
