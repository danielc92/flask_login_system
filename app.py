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

# SQL skeletons
select_skeleton = "SELECT * FROM users WHERE username_ = '{}'"
insert_skeleton = "INSERT INTO users (username_, passowrd_, firstname_, lastname_, email)\
             VALUES ('{}', '{}','{}','{}','{}')"

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
        
        users = pandas.read_sql_query(select_skeleton.format(posted_login), con = engine)

        print(users)
        if len(posted_login) == 0 or len(posted_password) == 0:
            error = "You must enter a username and password to login."
            return render_template('login.html', error = error)
        else:

            if users.shape[0] > 0:
                try:
                    database_password = users.loc[0, 'passowrd_']
                    print("Database password is {}, attempted password is {}".format(database_password, posted_password))
                    if database_password == posted_password:
                        session['logged_in'] = True
                        session['username'] = posted_login
                        print("user details are correct!")
                        return redirect(url_for('home'))
                except:
                    error = "Password is incorrect. Try again"
                    return render_template('login.html', error=error)
            else:
                error = "User does not exist"
                return render_template('login.html', error=error)

    return render_template('login.html')

def chkln(word):
    if len(word)>0:
        return True
    else:
        return False
# Register Route
@app.route('/register', methods = ['GET', 'POST'])
def register():

    error = None

    if request.method == "POST":

        r_username = request.form['rusername']
        r_password = request.form['rpassword']
        r_first = request.form['rfirst']
        r_last = request.form['rlast']
        r_email = request.form['remail']

        if chkln(r_username) ==True and chkln(r_password)==True and chkln(r_first)==True and chkln(r_last)==True and chkln(r_email)==True:
            
            conn = engine.connect()
            trans = conn.begin()
            conn.execute(insert_skeleton.format(r_username, 
                r_password,
                r_first,
                r_last,
                r_email))
            trans.commit()
            conn.close()

            time.sleep(3)
            return redirect(url_for('login'))
        else:
            error = "You must fill in all fields"
            return render_template('register.html', error = error)

    return render_template('register.html', error = "Enter details to register")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# Home Route
@app.route('/home')
@login_required
def home():
    return render_template('home.html', user = session['username'])

