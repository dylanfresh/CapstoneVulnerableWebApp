from app.forum import f
from flask import render_template

@f.route('/')
def index():
    return render_template('forum/forum.html')
