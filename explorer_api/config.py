import os
import secrets


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = secrets.token_urlsafe(30)
    JWT_SECRET_KEY = os.environ["JWT_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development environment configuration
    """

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """
    Production environment configuration
    """

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """
    Testing environment configuration
    """

    DEBUG = True
    TESTING = True


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
