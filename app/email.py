from flask import current_app, render_template
from flask_mail import  Message
from .  import mails

def send_mail(to,subject, template, **kwargs):
    # print("Имя модуля: ",__name__)
    """ отправка письма"""
    msg = Message(current_app.config["FLASKY_MAIL_SUBJECT_PREFIX"]+subject, 
    sender = current_app.config["FLASKY_MAIL_SENDER"], recipients=[to])
    # msg.body = render_template(template+".txt",**kwargs) # тестовая версия шаблона письма
    msg.html = render_template(template+".html",**kwargs) # HTML версия шаблона письма
    mails.send(msg)

def send_mail2(to,subject, template, **kwargs):
    # print("Имя модуля: ",__name__)
    """ отправка письма"""
    msg = Message(subject, sender = current_app.config["MAIL_SENDER"], recipients=[to])    
    msg.html = template # render_template(template,**kwargs) # HTML версия шаблона письма
    mails.send(msg)

