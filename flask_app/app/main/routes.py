from flask import render_template, request, redirect, url_for, current_app
from flask_app.app.main import bp

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/forum')
def forum():
    return render_template('forum.html')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action', 'login')

        if action == 'toggle':
            current_app.config["VULNERABLE"] = not current_app.config["VULNERABLE"]
            return redirect(url_for("main.login"))

        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if current_app.config["VULNERABLE"]:
            result = f"Vulnerable: {username}"
        else:
            result = f"Secure: {username}"

        return render_template("login.html",
                               mode="VULNERABLE" if current_app.config["VULNERABLE"] else "SECURE",
                               result=result,
                               username=username, )

    return render_template("login.html",
                           mode="VULNERABLE" if current_app.config["VULNERABLE"] else "SECURE",
                           result=None,
                           username='', )

