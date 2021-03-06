'''
This app will consist of a login, register and home page
using postgres as a backend system.

POSTGRES SCRIPT TO CREATE DATABASE FOR THIS APP

CREATE TABLE users
(
	id_ SERIAL PRIMARY KEY,
	username_ VARCHAR(255),
	password_ VARCHAR(255),
	firstname_ VARCHAR(255),
	lastname_ VARCHAR(255),
	email_ VARCHAR(255)
)

CREATE TABLE posts
(
	post_id_ SERIAL PRIMARY KEY,
	post_userid INTEGER,
	post_usermame VARCHAR(255),
	post_title VARCHAR(255),
	post_content TEXT,
	post_date VARCHAR(255),
	post_category VARCHAR(255)

)


'''

from flask import Flask,render_template,url_for,redirect,request,session
from datetime import timedelta
import datetime
from functools import wraps
import json
import pandas
from sqlalchemy import create_engine
import os
import time
import re
from string import ascii_letters
from string import digits
import hashlib

# Validator functions

def validate_password(p):

    invalid = True
    while invalid:
        if (len(p)<8 or len(p)>20):
            break
        elif not re.search("[a-z]",p):
            break
        elif not re.search("[0-9]",p):
            break
        elif not re.search("[A-Z]",p):
            break
        elif not re.search("[$#@]",p):
            break
        elif re.search("\s",p):
            break
        else:
            print("Valid Password")
            invalid=False
            break
            
    return invalid


def validate_human_name(name):
    
    invalid = False
    
    for char in name:
        if char in ascii_letters:
            continue
        else:
            invalid = True
            break
            
    return invalid

def validate_username(name):
    
    invalid = False
    
    for char in name:
        if char in (ascii_letters + digits):
            continue
        else:
            invalid = True
            break
            
    return invalid

def validate_email(email):
    
    invalid  = True
    
    while invalid:
        if len(email) < 7 or len(email) > 100:
            break
        elif email[-4:] != ".com":
            break
        elif email.count('@') != 1:
            break
        elif email.index('@') == 0 or email.index('@') == len(email)-1:
            break
        else:
            invalid = False
            break
    return invalid

# App config
app = Flask(__name__)
app.secret_key = 'jhgjjGDpifaj4904ufjajlwah89h392hi4lfknhflkh9842hfiu239h72h928b2ih2897b290f420j2khg2984hoklndjn2f3908h209d2'
app.debug = True

# Create database engine
engine = create_engine('postgresql://postgres:12345@localhost:5432/flask')

# SQL skeletons
select_skeleton = "SELECT * FROM users WHERE username_ = '{}'"
insert_skeleton = "INSERT INTO users (username_, password_, firstname_, lastname_, email_)\
             VALUES ('{}', '{}','{}','{}','{}')"


def encrypt(a_password):
    encrypted = hashlib.sha512(a_password.encode('utf-8')).hexdigest()
    return encrypted

# User exists
def user_exists(username):
    userlist = pandas.read_sql_query(select_skeleton.format(username), con = engine)
    if userlist.shape[0] > 0:
        return True
    else:
        return False

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
                database_password = users.loc[0, 'password_']
                user_id = int(users.loc[0, 'id_'])
                print("Database password is {}, attempted password is {}".format(database_password, posted_password))
                if database_password == encrypt(posted_password):
                    session['logged_in'] = True
                    session['username'] = posted_login
                    session['user_id'] = user_id
                    return redirect(url_for('home'))
                else:
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

        if chkln(r_username) ==True and \
        chkln(r_password)==True and \
        chkln(r_first)==True and \
        chkln(r_last)==True and \
        chkln(r_email)==True:
            

            if validate_username(r_username) == False:

                if user_exists(r_username) == False:

                    if validate_human_name(r_first) == False and validate_human_name(r_last) == False:
                        
                        if validate_email(r_email) == False:

                            if validate_password(r_password) == False:
                                conn = engine.connect()
                                trans = conn.begin()
                                conn.execute(insert_skeleton.format(r_username, encrypt(r_password), r_first, r_last, r_email))
                                trans.commit()
                                conn.close()
                                return redirect(url_for('login'))
                            else:
                                error = "Invalid password, passwords must contain at least 1 '@#$', 1 uppercase, 1 digit, 1 lowecase and be between  8-20 chars long."
                                return render_template('register.html', error = error)

                        else:
                            error = "Invalid email."
                            return render_template('register.html', error = error)

                    else:
                        error = "Invalid first or last name. Names can contain letters only."
                        return render_template('register.html', error = error)
                else:
                    error = "Username already exists"
                    return render_template('register.html', error = error)

            else:
                error = "Invalid username."
                return render_template('register.html', error = error)
  
        else:
            error = "You must fill in all fields"
            return render_template('register.html', error = error)

    return render_template('register.html')

# Log out Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# Default Route
@app.route('/')
def default():
    return redirect(url_for('home'))

# Home Route
@app.route('/home')
@login_required
def home():
    return render_template('home.html', session = session)

post_skeleton = "\
        INSERT INTO posts (post_userid, post_username, post_title, post_content, post_date, post_category) \
        VALUES ({}, '{}','{}','{}','{}', '{}')"

# Create post route
# This route will be accessible through button on Blog Route page
@app.route('/create-post', methods = ['GET', 'POST'])
@login_required
def create_post():

    p_error = None

    if request.method == 'POST':

        p_title = request.form['posttitle']
        p_content = request.form['postcontent']

        if len(p_title) >0 and len(p_content)>0:
            checksql = "SELECT post_title FROM posts WHERE post_title = '{}'"
            check_title = pandas.read_sql_query(checksql.format(p_title), con = engine)
            if check_title.shape[0] >0:
                p_error = "Post title exists."
            else:
                p_category = request.form['postcategory']
                p_userid = session['user_id']
                p_username = session['username']
                p_date = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")

                
                conn = engine.connect()
                trans = conn.begin()
                conn.execute(post_skeleton.format(p_userid, 
                    p_username,
                    p_title, 
                    p_content, 
                    p_date, 
                    p_category))
                trans.commit()
                conn.close()

                p_error = "Post created successfully!"
        else:

            p_error = "You must have a post title and post content."

    return render_template('create_post.html', session = session, p_error = p_error)

# Blog Route
@app.route('/blog', methods=['GET'])
@login_required
def blog():
    
    

    posts_dataframe = pandas.read_sql_query("SELECT * FROM posts", con = engine)
    posts = posts_dataframe.to_dict(orient = "records")

    print(posts)

    return render_template('blog.html', session = session, posts = posts)

