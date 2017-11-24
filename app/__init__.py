from flask import Flask, render_template, Blueprint
from flask_mail import Mail
from .main import main as main_blueprint

mail = Mail()

def create_app(config_name):
    app = Flask(__name__)

    mail.init_app(app)

    # здесь подключаются маршруты и нестандартные страницы с сообщениями об ошибках
    
    app.register_blueprint(main_blueprint)   # регистрация макета

    return app
