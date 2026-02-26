import os
from flask import Flask
from dotenv import load_dotenv
from src.routes.main import bp as main_bp
from src.routes.auth import bp as auth_bp
from src.database import init_db

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-change-me')

    init_db()
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
