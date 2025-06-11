from flask import Flask
from src.routes.main import bp as main_bp

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dev'
    app.register_blueprint(main_bp)
    
    return app