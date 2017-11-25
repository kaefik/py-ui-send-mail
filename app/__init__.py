from flask import Flask, render_template, Blueprint
from flask_mail import Mail
from .main import main as main_blueprint
from config import config

mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    

    mail.init_app(app)

    # здесь подключаются маршруты и нестандартные страницы с сообщениями об ошибках
    
    app.register_blueprint(main_blueprint)   # регистрация макета

    return app
