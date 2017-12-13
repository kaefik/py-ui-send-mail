""" Хранение настроек приложения """

import os
import csv
import configparser

base_dir = os.path.abspath(os.path.dirname(__file__))

path_template_mail = "template_mail"

namefile_cfg = "config.ini"

config = configparser.ConfigParser()
config.read(namefile_cfg)

def str2bool(str):
    if str.lower() == "true":
        return True
    else:
        return False



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
    DEBUG=True
    MAIL_SERVER = str(config['MAIL']['MAIL_SERVER'])
    MAIL_PORT = int(config['MAIL']['MAIL_PORT'])
    MAIL_USE_TLS = str2bool(config['MAIL']['MAIL_USE_TLS'])
    MAIL_USE_SSL = str2bool(config['MAIL']['MAIL_USE_SSL'])
    MAIL_USERNAME = config['MAIL']['MAIL_USERNAME']
    MAIL_PASSWORD = config['MAIL']['MAIL_PASSWORD']


class TestingConfig(Config):
    TESTING = True

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
    }
