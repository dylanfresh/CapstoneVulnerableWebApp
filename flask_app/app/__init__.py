from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(): #config_class=Config
    '''Function to use as a factory and house all the blueprints'''
    app = Flask(__name__)
    app.config.from_object(Config)

    # database set up
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask extensions here

    # Register blueprints here
    from flask_app.app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from flask_app.app.forum import f as forum
    app.register_blueprint(forum)

    # Home page route (non-blueprint is OK)
    @app.route('/')
    def index():
        return "Home page (replace with template later)"
 
    return app
