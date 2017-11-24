""" Хранение настроек приложения """

import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"
    FLASKY_MAIL_SENDER = "Flasky Admin <ilnursoft@gmail.com>"
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.google.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class TestingConfig(Config):
    TESTING = True

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
    }
