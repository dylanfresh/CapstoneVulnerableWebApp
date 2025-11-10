import os
import pymysql
from flask import Flask, request, session, render_template_string, g

"""
app.py: WSRP web application entry point

Implements proto-SQL injection example for CS461: Progress
Report #2

References:
- https://cwe.mitre.org/data/definitions/89.html
- https://flask.palletsprojects.com/en/stable/quickstart/
- https://flask.palletsprojects.com/en/stable/templating/
- https://pymysql.readthedocs.io/en/latest/user/examples.html
- https://www.postgresql.org/docs/current/tutorial-install.html
- https://pypi.org/project/PyMySQL/
- https://www.geeksforgeeks.org/python/flask-http-methods-handle-get-post-requests/
- https://realpython.com/prevent-python-sql-injection/
- https://medium.com/@technicalpanchayat18/flask-pymysql-introduction-ae00ab1821f
- https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html 
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Sending_and_retrieving_form_data
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input
"""

tmp_db = "sql_injection_tmp"

app = Flask(__name__)

# ---------------------- HTML Helpers ----------------------
html_form = """
<h2>{{title}}</h2>
<p>
    <a href="/">Home</a> |
    <a href="/vulnerable_login">Vulnerable login</a> |
    <a href="/secure_login">Secure login</a>
</p>
<form method="post">
    Username: <input name="username">
    Password: <input name="password" type="password">
    <input type="submit" value="Login">
</form>
<h3>Result</h3>
<p>{{ result }}</p>
"""


# ---------------------- DB Helpers ----------------------
"""
These helper functions are based on "PyMySQL 1.1.2" from pypi.org 
(https://pypi.org/project/PyMySQL/) and "Flask + PyMySQL: Introduction" 
from Medium (https://medium.com/@technicalpanchayat18/flask-pymysql-introduction-ae00ab1821f)

Notes: may need to be refactored to accommodate potential changes in
database (PostGreSQL, MySQL, etc.) and developments in SQL injection
testing and mitigation
"""
def connect_db(db=None):
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="tmp_user",
        password="tmp_pass",
        database=tmp_db,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def get_db():
    if "db" not in g:
        g.db = connect_db()

    return g.db


def close_db(exc):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    connect = connect_db()

    try:
        with connect.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{tmp_db}` DEFAULT CHARACTER SET utf8mb4;")
            cursor.execute(f"USE `{tmp_db}`;")
            cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                           "id INT AUTO_INCREMENT PRIMARY KEY, "
                           "username VARCHAR(100) UNIQUE,"
                           "password VARCHAR(255), "
                           "role VARCHAR(50)) ENGINE=InnoDB;")
            cursor.execute("SELECT COUNT(*) AS count FROM users;")

            tmp = cursor.fetchall()
            count = tmp[0]['count']

            if count == 0:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ("jane", "janed", "user"))
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ("john", "johnd", "user"))
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ("mary", "maryp", "user"))
    finally:
        connect.close()


# ---------------------- Pages ----------------------
@app.route('/')
def helloWorld():
    return """
<h2>Hello, World!</h2>
<p>
    <a href="/">Home</a> |
    <a href="/vulnerable_login">Vulnerable login</a> |
    <a href="/secure_login">Secure login</a>
</p>
"""


@app.route('/vulnerable_login', methods=["GET", "POST"])
def vulnerable_login():
    """
    Login endpoint prototype VULNERABLE:

    This implementation is based on "SQL Injection in Python" from SecureFlag
    (https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html)
    and "Preventing SQL Injection Attacks With Python" from RealPython
    (https://realpython.com/prevent-python-sql-injection/)

    Notes: may need to be refactored to accommodate potential changes in
    database (PostGreSQL, MySQL, etc.) and developments in SQL injection
    testing and mitigation
    """
    result = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        db = get_db()
        with db.cursor() as cursor:
            query = f"SELECT id, username, role FROM users WHERE username='{username}' AND password='{password}';"

            try:
                cursor.execute(query)
                rows = cursor.fetchall()

                if rows:
                    out = "\n".join(f"id={r['id']} username={r['username']} role={r['role']}" for r in rows)
                else:
                    out = "No matching users"
                result = f"Executed SQL: \n {query} \n Output: \n {out}"
            except Exception:
                result = f"SQL error: {Exception}"

    return render_template_string(html_form, title="SQL Injection: Vulnerable \
                                    Demo", result=result)


@app.route('/secure_login', methods=["GET", "POST"])
def secure_login():
    """
    Login endpoint prototype SECURE:

    This implementation is based on "SQL Injection in Python" from SecureFlag
    (https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html)
    and "Preventing SQL Injection Attacks With Python" from RealPython
    (https://realpython.com/prevent-python-sql-injection/)

    Notes: may need to be refactored to accommodate potential changes in
    database (PostGreSQL, MySQL, etc.) and developments in SQL injection
    testing and mitigation
    """
    result = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        db = get_db()

        with db.cursor() as cursor:
            query = "SELECT id, username, role FROM users WHERE username=%s AND password=%s;"

            try:
                cursor.execute(query, (username, password))
                rows = cursor.fetchall()

                if rows:
                    out = "\n".join(f"id={r['id']} username={r['username']} role={r['role']}" for r in rows)
                else:
                    out = "No matching users"
                result = f"Executed SQL: \n {query} \n Output: \n {out}"
            except Exception:
                result = f"SQL error: {Exception}"

    return render_template_string(html_form, title="SQL Injection: Secure", result=result)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
