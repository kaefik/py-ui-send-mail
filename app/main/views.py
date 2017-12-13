from flask import render_template, session, redirect, url_for, request
from . import main
from ..forms import CreateEmailTemplateForm
from ..email import send_mail
import configparser


def createConfigMailTemplate(path,subject_mail,message_mail):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("TEMPLATEMAIL")
    config.set("TEMPLATEMAIL", "subject",subject_mail)           
    config.set("TEMPLATEMAIL", "template",message_mail)
    with open(path, "w") as config_file:
        config.write(config_file)
    return True
    

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/send")
def send():
    send_mail("ilnursoft@yandex.ru","test mail", "template_email")
    return redirect(url_for("index"))

@main.route("/create-template", methods=['GET', 'POST'])
def create_template():
    form = CreateEmailTemplateForm(request.form)
    if request.method == "POST":        
       form = CreateEmailTemplateForm(request.form)
    if (request.method == "POST") and form.validate():        
        
        subjectmail = str(request.form["subjectmail"])
        messagemail = str(request.form["messagemail"])  
        createConfigMailTemplate("template1.cfg",subjectmail,messagemail)
        
        """
        if result is None:
            flash("Пользователь не найден или неверный пароль", "error")
        else:
            result_verify = result.verify_password(password_user)
            if result_verify:
                session["logged_in"] = True
                session["username"] = username
                session["role"] = result.role.name
                flash("Вы вошли, как {}".format(username), "success")
                return redirect(url_for("view"))
            else:
                flash("Пользователь не найден или неверный пароль", "error")
                """
    return render_template("create-template.html",form=form)


@main.route("/create-maillist")
def create_maillist():
    return render_template("create-maillist.html")