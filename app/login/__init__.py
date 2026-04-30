from flask import Blueprint

l = Blueprint(
    'login',
    __name__,
    url_prefix='/login'
)

from app.login import routes