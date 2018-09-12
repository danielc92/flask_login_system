'''
This app will consist of a login, register and home page
using postgres as a backend system.
'''

from flask import Flask,render_template,url_for,redirect,request,session
from datetime import timedelta
from functools import wraps
import json
import os

# App config
app = Flask(__name__)
app.secret_key = 'jhgjjGDpifaj4904ufjajlwah89h392hi4lfknhflkh9842hfiu239h72h928b2ih2897b290f420j2khg2984hoklndjn2f3908h209d2'
app.debug = True


# Login Required function
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        
        if test_username == login and test_password == password:

            print(test_username + ' has logged in successfully.')
            session['logged_in'] = True
            session['user'] = login
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Try again'
            return render_template('login.html', error=error)

    return render_template('login.html', error=error)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')