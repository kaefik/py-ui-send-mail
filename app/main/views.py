from flask import render_template, session, redirect, url_for, request, flash
from . import main
from ..forms import CreateEmailTemplateForm, CreateEmailListSenderForm, CreateTaskForm
from ..email import send_mail2
import configparser
from os import listdir
import os

path_absolute = "app/templates/"
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

# кандидат на удаление
def create_cfg_task(path, id_maillist=-1,id_template=-1):
    """
        Создание конфигурационного файла для задачи которую нужно выполнить, возвращает путь созданного задания отправки
        файл задачи содержит только номера файлов списка рассылки и шаблоны письма
    """
    if (id_maillist==-1) and (id_template==-1):
        return False

    config = configparser.ConfigParser()
    config.add_section("TASK")
    config.set("TASK", "maillist",id_maillist)           
    config.set("TASK", "templatemail",id_template)           
    with open(path, "w") as config_file:
        config.write(config_file)
    return path

def create_cfg_task_full(path, id_maillist=-1,id_template=-1,nametask="Безназвания"):
    """
        Создание конфигурационного файла для задачи которую нужно выполнить, возвращает путь созданного задания отправки
        файл задачи содержит содержимое списка рассылки и шаблона письма
    """
    if (id_maillist==-1) and (id_template==-1):
        return False

    maillist = get_cfg_maillist(path_absolute+path_sender_list+id_maillist)
    templatemail = get_cfg_templatemail(path_absolute+path_template_mail+id_template)
   
    config = configparser.ConfigParser()
    config.add_section("TASK")
    config.set("TASK", "nametask",nametask)
    config.add_section("SENDERMAILLIST")
    config.set("SENDERMAILLIST", "namelist",maillist["name"])
    config.set("SENDERMAILLIST", "adresslist",maillist["data"])
    config.add_section("TEMPLATEMAIL")
    config.set("TEMPLATEMAIL", "subject",templatemail["subject"])
    config.set("TEMPLATEMAIL", "template",templatemail["template"])
    with open(path, "w") as config_file:
        config.write(config_file)   
    return path

# кндидат на удаление
def get_cfg_task_old(path):
    """
        получение содержимого из файла конфигурации
    """
    result=dict()
    data_cfg = configparser.ConfigParser()
    data_cfg.read(path)        
    result["maillist"] = data_cfg['TASK']['maillist']
    result["templatemail"] = data_cfg['TASK']['templatemail']
    return result

def get_cfg_task(path):
    """
        получение содержимого из файла конфигурации
    """
    result=dict()
    data_cfg = configparser.ConfigParser()
    data_cfg.read(path)        
    result["nametask"] = data_cfg['TASK']['nametask']
    result["namelist"] = data_cfg['SENDERMAILLIST']['namelist']
    result["adresslist"] = data_cfg['SENDERMAILLIST']['adresslist']
    result["subject"] = data_cfg['TEMPLATEMAIL']['subject']
    result["template"] = data_cfg['TEMPLATEMAIL']['template']
    return result

def get_cfg_maillist(path):
    """
        получение содержимого из файла конфигурации списка рассылки
    """
    result=dict()
    data_cfg = configparser.ConfigParser()
    data_cfg.read(path)        
    result["data"] = data_cfg['SENDERMAILLIST']['adresslist']
    result["name"] = data_cfg['SENDERMAILLIST']['namelist']
    return result

def get_cfg_templatemail(path):
    """
        получение содержимого из файла конфигурации шаблона письма
    """
    result=dict()
    data_cfg = configparser.ConfigParser()
    data_cfg.read(path)        
    result["subject"] = data_cfg['TEMPLATEMAIL']['subject']
    result["template"] = data_cfg['TEMPLATEMAIL']['template']
    return result

def generate_filename(path=path_absolute+path_sender_list):
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

def get_all_files(path=path_absolute+path_sender_list):
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

def get_content_files(path=path_absolute+path_sender_list):
    """ 
        получение содержимое всех файлов из папки path   ???? - кандидат на удаление
    """
    content_files = []
    files = get_all_files(path)
    for name_file in files:
        with open(path+name_file,"r") as f:
            content_files.append((name_file,f.read()))
    return content_files


def get_content_templatemail(path=path_absolute+path_template_mail):
    """
        получение содержимое конфиг файла шаблонов писем
    """
    data_templatemail = list()
    file_names = listdir(path)
    # print(file_names)   
    
    for i in file_names:
        namefile = path+i
        dict_data_maillist = get_cfg_templatemail(namefile)
        dict_data_maillist["name_file"] = i
        data_templatemail.append(dict_data_maillist)    
    return data_templatemail

def get_content_maillist(path=path_absolute+path_sender_list):
    """
        получение содержимое конфиг файла списков рассылки
    """
    file_names = listdir(path)
    # print(file_names)
 
    data_maillist = list()
    for i in file_names:
        namefile = path+i      
        dict_data_maillist = get_cfg_maillist(namefile)      
        dict_data_maillist["name_file"] = i
        data_maillist.append(dict_data_maillist) 
    return data_maillist

# кандидат на удаление
def send_mail_from_task_old(filename_task): 
    """
        если задача обработана, возращается True и файл задачи переносится в папку data/task/done
    """
    # разбор файла конфигурации задачи
    cfg_task = get_cfg_task(filename_task)
    maillist = get_cfg_maillist(path_absolute+path_sender_list+cfg_task["maillist"])
    templatemail = get_cfg_templatemail(path_absolute+path_template_mail+cfg_task["templatemail"])
    print("templatemail = ",templatemail)
    array_maillist = maillist["data"].split("\n")
    # print("array_maillist = ",array_maillist)
    for address in array_maillist:
        send_mail2(address,templatemail["subject"],templatemail["template"])
    return True

def send_mail_from_task(filename_task):
    """
        если задача обработана, возращается True 
    """
    # разбор файла конфигурации задачи
    cfg_task = get_cfg_task(filename_task)
    maillist = cfg_task["adresslist"]
    templatemail = cfg_task["template"]    
    array_maillist = maillist.split("\n")    
    try:
        for address in array_maillist:
            send_mail2(address,cfg_task["subject"],cfg_task["template"])
    except Exception:
        return False    
    return True

# --------- маршруты

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
        createConfigMailTemplate(path_absolute+path_template_mail+generate_filename(path_absolute+path_template_mail),subjectmail,messagemail)
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
        createConfigMailSender(path_absolute+path_sender_list+generate_filename(path_absolute+path_sender_list),sendermail,name_maillist)
        flash("Создан новый список рассылки","success")
        return redirect(url_for(".index"))
    return render_template("create-maillist.html", form=form)

@main.route("/create-task", methods=['GET', 'POST'])
def create_task():
    form = CreateTaskForm(request.form)        

    dict_data_maillist = get_content_maillist(path_absolute+path_sender_list)    
    dict_data_template = get_content_templatemail(path_absolute+path_template_mail)

    print("dict_data_maillist = ", dict_data_maillist)

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
        name_task = request.form["name_task"]
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

        filename_task = create_cfg_task_full(path_absolute+path_task+generate_filename(path_absolute+path_task),id_select_maillist,id_select_template,name_task)
        
        if filename_task!=False:  # проверяем создана ли задача           
            send_mail_from_task(filename_task)
            # после выполнения рассылки задача перемещается в папку done и 
            # имя задачи менятся на дату и время начала выполнения задачи
            ar = os.path.split(filename_task)                        
            os.rename(filename_task,"app/templates/data/task_done/"+ar[-1])
        

        flash("Создана новая задача на отправку","success")
        return redirect(url_for(".index"))
    return render_template("create-task.html", form=form, data_maillist=dict_data_maillist,data_templatemail=dict_data_template)


@main.route("/view-maillist")
def view_maillist():
    data_maillist = get_content_maillist(path_absolute+path_sender_list)
    return render_template("view-maillist.html",data=data_maillist)

@main.route("/view-templatemail")
def view_templatemail():    
    data_templatemail = get_content_templatemail(path_absolute+path_template_mail)           
    return render_template("view-templatemail.html",data=data_templatemail)

@main.route("/about")
def about():
    return render_template("about.html")

# --------- END маршруты