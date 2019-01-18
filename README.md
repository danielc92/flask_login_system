# Flask Login System
Creating a simple login system for a `flask` web application which is able to authenticate users into particular routes within the application.

# Before you get started
Should have a basic understanding of web applications, requests (POST/GET) and basic python skills. You should also understand how ORM works (`sqlalchemy`) and the concept of hashing passwords with `hashlib`. The backend database for this project is `postgres`, an open source free to use relational database.

# Setup
**How to obtain this repository:**
```sh
git clone https://github.com/danielc92/flask_login_system.git
```
**Modules/dependencies:**
- `flask`
- `sqlalchemy`
- `pandas`
- `hashlib`
- Installation of `postgres` database (alternatively you can use `sqlite3`)


Install the following dependences:
```sh
pip install flask sqlalchemy pandas hashlib
```

To run locally:
```sh
python3 main.py
```

# Tests
- Testing posting user credentials through login page
- Validated data sent through post
- Cross check data validated vs data hashed in database
- Users can log in successfully

# Contributors
- Daniel Corcoran

# Sources
- [flask documentation](http://flask.pocoo.org/)