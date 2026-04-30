from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/forum.html')
def forum():
    return render_template('forum.html')

@bp.route('/login.html')
def login():
    return render_template('login.html')

