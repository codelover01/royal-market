import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

# Application Configurations
class Config:
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    JWT_ACCESS_CSRF_HEADER_NAME = ['X-CSRFToken']
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 30 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = "Bearer"
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_ACCESS_CSRF_FIELD_NAME = "csrf_token"
    JWT_QUERY_STRING_NAME = "jwt_token"
    JWT_QUERY_STRING_VALUE_PREFIX = ""


    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

    # Email setup configuartions
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


class TestConfig(Config):
    TESTING = os.getenv("TESTING")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_TEST")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

