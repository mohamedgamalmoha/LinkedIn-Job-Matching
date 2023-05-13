import os
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

# Get configuration variable
DEBUG = os.environ.get('DEBUG')

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'),
    'SQLALCHEMY_DATABASE_URI': os.environ.get('SQLALCHEMY_DATABASE_URI'),
    'WTF_CSRF_ENABLED': os.environ.get('WTF_CSRF_ENABLED'),
    'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
    'JWT_IDENTITY_CLAIM': 'id',
})


login_manager = LoginManager(app)
login_manager.login_view = 'login'

jwt = JWTManager(app)
db = SQLAlchemy(app)


from web import routs
