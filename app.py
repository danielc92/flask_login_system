'''
This app will consist of a login, register and home page
using postgres as a backend system.
'''

from flask import Flask,render_template,url_for,redirect,request,session
from datetime import timedelta
from functools import wraps
import json
import pandas
from sqlalchemy import create_engine
import os
import time

# App config
app = Flask(__name__)
app.secret_key = 'jhgjjGDpifaj4904ufjajlwah89h392hi4lfknhflkh9842hfiu239h72h928b2ih2897b290f420j2khg2984hoklndjn2f3908h209d2'
app.debug = True

# Create database engine
engine = create_engine('postgresql://danielcorcoran@localhost:5432/flask')

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
    # Reset Error
    error = None

    if request.method == 'POST':
        
        posted_login = request.form['username']
        posted_password = request.form['password']
        select_skeleton = "SELECT * FROM users WHERE username_ = '{}'"
        users = pandas.read_sql_query(select_skeleton.format(posted_login), con = engine)

        print(users)
        if len(posted_login) == 0 or len(posted_password) == 0:
            error = "You must enter a username and password to login."
            return render_template('login.html', error = error)
        else:

            if users.shape[0] > 0:
                try:
                    database_password = users.loc[0, 'passowrd_']
                    print(database_password)
                    session['logged_in'] = True
                    session['username'] = posted_login
                    return render_template('home.html', user = session['username'])
                except:
                    error = "Password is incorrect. Try again"
                    return render_template('login.html', error=error)
            else:
                error = "User does not exist"
                return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')