from flask import Blueprint

f = Blueprint(
    'forum',
    __name__,
    url_prefix='/forum'
)

from app.forum import routes