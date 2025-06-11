from flask import Flask
from src.routes.main import bp as main_bp
from src.database import init_db

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dev'

    init_db()
    app.register_blueprint(main_bp)
    
    return app