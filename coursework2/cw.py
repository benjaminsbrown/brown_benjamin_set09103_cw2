from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Username and/or Password please try again.'
            else:
                session['Logged_in'] = True
                return redirect(url_for('home'))
                return render_template('home.html', error=error)
@app.route('/logout')
def logout():
        session.pop('Logged_in', None)
        return redirect(url_for('home'))
        return render_template('home.html'), 200
@app.route('/home')
def home():
	       return render_template('home.html'), 200
@app.route('/signup')
def signup():
	       return render_template('signup.html'), 200
