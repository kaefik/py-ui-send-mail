from flask import render_template, session, redirect, url_for, request, flash
from . import main
from ..forms import CreateEmailTemplateForm, CreateEmailListSenderForm, CreateTaskForm
from ..email import send_mail
import configparser
from os import listdir
import os


path_template_mail = "data/template_mail/"  # пусть где хранятся шаблоны писем
path_sender_list = "data/sender_list/"  # пусть где хранятся списки отправки
path_task = "data/task/"  # пусть где хранятся задачи

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

def createConfigMailSender(path,sender_mail,name_list):
    """
    Create a config file для списка рассылки
    """
    config = configparser.ConfigParser()
    config.add_section("SENDERMAILLIST")
    config.set("SENDERMAILLIST", "namelist",name_list)           
    config.set("SENDERMAILLIST", "adresslist",sender_mail)           
    with open(path, "w") as config_file:
        config.write(config_file)
    return True

def create_cfg_task(path, id_maillist=-1,id_template=-1):
    """
        Создание конфигурационного файла для задачи которую нужно выполнить
    """
    if (id_maillist==-1) and (id_template==-1):
        return False

    config = configparser.ConfigParser()
    config.add_section("TASK")
    config.set("TASK", "maillist",id_maillist)           
    config.set("TASK", "templatemail",id_template)           
    with open(path, "w") as config_file:
        config.write(config_file)
    return True


def generate_filename(path=path_sender_list):
    """
      генерация имени файла, имена файлов номер_по_порядку
    """
    filename=""
    if not os.path.exists(path):
        os.mkdir(path)
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

def get_all_files(path=path_sender_list):
    """
      возвращает все имена файлов в папке path
    """
    filename=""
    if not os.path.exists(path):
        os.mkdir(path)
    file_names = listdir(path)
    # print(file_names)
   # if file_names == []:
    #    return "1"    
       
    return file_names

def get_content_files(path=path_sender_list):
    """ 
        получение содержимое всех файлов из папки path   ???? - кандидат на удаление
    """
    content_files = []
    files = get_all_files(path)
    for name_file in files:
        with open(path+name_file,"r") as f:
            content_files.append((name_file,f.read()))
    return content_files


def get_content_templatemail(path=path_template_mail):
    """
        получение содержимое конфиг файла шаблонов писем
    """
    data_templatemail = list()
    file_names = listdir(path)
    # print(file_names)   
    
    for i in file_names:
        dict_data_maillist = dict()
        dict_data_maillist["name_file"] = i
        namefile = path+i

        data_cfg = configparser.ConfigParser()
        data_cfg.read(namefile)        
        dict_data_maillist["subject"] = data_cfg['TEMPLATEMAIL']['subject']
        dict_data_maillist["template"] = data_cfg['TEMPLATEMAIL']['template']

        data_templatemail.append(dict_data_maillist)    
    return data_templatemail

def get_content_maillist(path=path_sender_list):
    """
        получение содержимое конфиг файла списков рассылки
    """
    file_names = listdir(path)
    # print(file_names)
 
    data_maillist = list()
    for i in file_names:
        dict_data_maillist = dict()
        dict_data_maillist["name_file"] = i
        namefile = path+i

        data_cfg = configparser.ConfigParser()
        data_cfg.read(namefile)        
        dict_data_maillist["data"] = data_cfg['SENDERMAILLIST']['adresslist']
        dict_data_maillist["name"] = data_cfg['SENDERMAILLIST']['namelist']
        data_maillist.append(dict_data_maillist)       

    return data_maillist


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
        name_maillist = str(request.form["name_maillist"])
        createConfigMailSender(path_sender_list+generate_filename(path_sender_list),sendermail,name_maillist)
        flash("Создан новый список рассылки","success")
        return redirect(url_for(".index"))
    return render_template("create-maillist.html", form=form)

@main.route("/create-task", methods=['GET', 'POST'])
def create_task():
    d = [(1,'одsн'),(2,'два')] 
    form = CreateTaskForm(request.form)        

    dict_data_maillist = get_content_maillist(path_sender_list)
    dict_data_template = get_content_templatemail(path_template_mail)

    # генерация списка выбора списка рассылки
    choices_maillist =[] # get_content_files(path_template_mail)    
    for el in dict_data_maillist:
        choices_maillist.append((el["name_file"],el["name"]))    


    choices_template = [] # get_content_files(path_sender_list)     
    for el in dict_data_template:
        choices_template.append((el["name_file"],el["subject"])) 
       

    form.set_selectfield_maillist(selection_choices=choices_maillist)
    form.set_selectfield_templatemail(selection_choices=choices_template)
    if (request.method == "POST") and form.validate():        
        id_select_maillist = request.form["name_maillist"]
        id_select_template = request.form["name_templatemail"]
        # print("id_select_maillist = ",id_select_maillist)
        # print("id_select_template = ",id_select_template)
        if (id_select_maillist==-1) or (id_select_template==-1):
            flash("Невозможно создать задачу на отправку","error")
            return redirect(url_for(".index"))
        select_maillist = ""
        for el in dict_data_maillist:
            if el["name_file"]==id_select_maillist:
                select_maillist = el
        select_template=""
        for el in dict_data_template:
            if el["name_file"]==id_select_template:
                select_template = el

        create_cfg_task(path_task+generate_filename(path_task),id_select_maillist,id_select_template)
        flash("Создана новая задача на отправку","success")
        return redirect(url_for(".index"))
    return render_template("create-task.html", form=form, data_maillist=dict_data_maillist,data_templatemail=dict_data_template)


@main.route("/view-maillist")
def view_maillist():
    data_maillist = get_content_maillist(path_sender_list)
    return render_template("view-maillist.html",data=data_maillist)

@main.route("/view-templatemail")
def view_templatemail():    
    data_templatemail = get_content_templatemail(path_template_mail)           
    return render_template("view-templatemail.html",data=data_templatemail)

@main.route("/about")
def about():
    return render_template("about.html")