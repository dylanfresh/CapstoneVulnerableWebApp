from flask import Flask
from app.config import Config

def create_app(): #config_class=Config
    '''Function to use as a factory and house all the blueprints'''
    app = Flask(__name__)
    # app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.forum import f as forum
    app.register_blueprint(forum)

    # Home page route (non-blueprint is OK)
    @app.route('/')
    def index():
        return "Home page (replace with template later)"
 
    return app
