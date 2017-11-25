""" Хранение настроек приложения """

import os
import csv
base_dir = os.path.abspath(os.path.dirname(__file__))


namefile_cfg = "configs.cfg"

def get_csv_file(namefile_cfg):
    name_user =""
    pass_user = ""
    with open(namefile_cfg, newline='') as csvfile:
        str = csv.reader(csvfile, delimiter=';')
        for row in str:
            name_user = row[0]
            pass_user = row[1]
    return name_user,pass_user

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
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS  = False
    MAIL_USE_SSL  = True
    MAIL_USERNAME, MAIL_PASSWORD = get_csv_file(namefile_cfg)


class TestingConfig(Config):
    TESTING = True

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
    }
