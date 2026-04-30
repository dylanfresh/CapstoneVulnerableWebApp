from app.login import l
from flask import render_template, request, current_app
from sqlalchemy import text
from app import db


@l.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if current_app.config['VULNERABLE_MODE']:
        # intentionally vulnerable
        query = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        result = db.session.execute(text(query))
    else:
        # secure version
        query = text("SELECT * FROM user WHERE username = :username AND password = :password")
        result = db.session.execute(query, {
            "username": username,
            "password": password
        })

    user = result.fetchone()

    if user:
        return {"success": True}
    else:
        return {"success": False}
    