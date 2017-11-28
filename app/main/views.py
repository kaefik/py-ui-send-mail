from flask import render_template, session, redirect, url_for
from . import main
from ..email import send_mail

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/send")
def send():
    send_mail("ilnursoft@yandex.ru","test mail", "template_email")
    return redirect(url_for("index"))

@main.route("/create-template")
def create_template():
    return render_template("create-template.html")


@main.route("/create-maillist")
def create_maillist():
    return render_template("create-maillist.html")