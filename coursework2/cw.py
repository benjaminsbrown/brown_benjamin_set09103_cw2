from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def root():
	return render_template('home.html'), 200
@app.route('/signup')
def signup():
	return render_template('signup.html'), 200
