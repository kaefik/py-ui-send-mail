from flask import render_template, session, redirect, url_for, request, flash
from . import main
from ..forms import CreateEmailTemplateForm, CreateEmailListSenderForm
from ..email import send_mail
import configparser
from os import listdir


path_template_mail = "data/template_mail/"  # пусть где хранятся шаблоны писем
path_sender_list = "data/sender_list/"  # пусть где хранятся списки отправки

def createConfigMailTemplate(path,subject_mail,message_mail):
    """ 
    Create a config file для шаблона письма
    """
    config = configparser.ConfigParser()
    config.add_section("TEMPLATEMAIL")
    config.set("TEMPLATEMAIL", "subject",subject_mail)           
    config.set("TEMPLATEMAIL", "template",message_mail)
    with open(path, "w") as config_file:
        config.write(config_file)
    return True

def createConfigMailSender(path,sender_mail):
    """
    Create a config file для списка рассылки
    """
    config = configparser.ConfigParser()
    config.add_section("SENDERMAILLIST")
    config.set("SENDERMAILLIST", "adresslist",sender_mail)           
    with open(path, "w") as config_file:
        config.write(config_file)
    return True

def generate_filename(path):
    """
      генерация имени файла, имена файлов номер_по_порядку
    """
    filename=""
    file_names = listdir(path)
    # print(file_names)
    if file_names == []:
        return "1"

    max_int = 0
    for i in file_names:
        if max_int<int(i):
            max_int = int(i)    
    filename = str(max_int+1) 
       
    return filename
    

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/send")
def send():
    send_mail("ilnursoft@yandex.ru","test mail", "template_email")
    return redirect(url_for(".index"))

@main.route("/create-template", methods=['GET', 'POST'])
def create_template():
    form = CreateEmailTemplateForm(request.form)
    if request.method == "POST":        
       form = CreateEmailTemplateForm(request.form)
    if (request.method == "POST") and form.validate():    
        subjectmail = str(request.form["subjectmail"])
        messagemail = str(request.form["messagemail"])  
        createConfigMailTemplate(path_template_mail+generate_filename(path_template_mail),subjectmail,messagemail)
        flash("Создан новый шаблон сообщения","success")
        return redirect(url_for(".index"))
    return render_template("create-template.html",form=form)


@main.route("/create-maillist", methods=['GET', 'POST'])
def create_maillist():
    form = CreateEmailListSenderForm(request.form)
    if request.method == "POST":        
       form = CreateEmailListSenderForm(request.form)
    if (request.method == "POST") and form.validate():        
        sendermail = str(request.form["sendermail"])
        createConfigMailSender(path_sender_list+generate_filename(path_sender_list),sendermail)
        flash("Создан новый список рассылки","success")
        return redirect(url_for(".index"))
    return render_template("create-maillist.html", form=form)

@main.route("/about")
def about():
    return render_template("about.html")