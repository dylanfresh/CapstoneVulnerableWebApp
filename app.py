import pymysql
from flask import Flask, request, session

"""
app.py: WSRP web application entry point

Implements proto-SQL injection example for CS461: Progress
Report #2

References:
- https://cwe.mitre.org/data/definitions/89.html
- https://flask.palletsprojects.com/en/stable/quickstart/
- https://pymysql.readthedocs.io/en/latest/user/examples.html
- https://www.postgresql.org/docs/current/tutorial-install.html
"""

app = Flask(__name__)


@app.route('/')
def helloWorld():
    return 'Hello, World!'


@app.route('/login')
def login():
    """
    Login endpoint prototype:

    This implementation is based on "SQL Injection in Python" from SecureFlag
    (https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html)
    and "Preventing SQL Injection Attacks With Python" from RealPython

    Notes: will need to be refactored to accommodate potential changes in
    database (PostGreSQL, MySQL, etc.) and developments in SQL injection
    testing and mitigation
    """
    username = request.values.get('username')
    password = request.values.get('password')

    db = pymysql.connect("localhost")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = \
                    '%s'" % (username, password))

    record = cursor.fetchone() 
    if record:
        session['logged_user'] = username

    db.close()


@app.route('/secure/login')
def secure_login():
    """
    Login endpoint prototype SECURE:

    This implementation is based on "SQL Injection in Python" from SecureFlag
    (https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html)
    and "Preventing SQL Injection Attacks With Python" from RealPython

    Notes: will need to be refactored to accommodate potential changes in
    database (PostGreSQL, MySQL, etc.) and developments in SQL injection
    testing and mitigation
    """
    username = request.values.get('username')
    password = request.values.get('password')

    db = pymysql.connect("localhost")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = \
                    %s" % (username, password))

    record = cursor.fetchone()
    if record:
        session['logged_user'] = username

    db.close()



if __name__ == '__main__':
    app.run(debug=True)

