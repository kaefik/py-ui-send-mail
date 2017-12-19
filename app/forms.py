from wtforms import Form, StringField, SubmitField, TextAreaField, SelectField, validators

# классы форм
class CreateEmailTemplateForm(Form):
    """ форма добавления/редактирования шаблона письма """
    subjectmail = StringField("Тема письма", [validators.Length(min=5, max=100)])
    messagemail = TextAreaField("Содержание письма", [validators.Length(min=5)])    
    submit = SubmitField("Сохранить")

class CreateEmailListSenderForm(Form):
    """ форма добавления/редактирования списка получателей письма """    
    name_maillist = StringField("Название списка", [validators.Length(min=5, max=100)])
    sendermail = TextAreaField("Список получателей рассылки", [validators.Length(min=5)])    
    submit = SubmitField("Сохранить")

class CreateTaskForm(Form):
    """ форма добавления задачи на отправку писем             
            data_maillist - список выбора списков рассылки   [(1,'one'),(2,'two')] 
            data_templatemail - список выбора шаблонов письма
        """        
    name_maillist = SelectField('Список рассылки')
    name_templatemail = SelectField('Шаблон письма ', default=1, choices=[(1,'one'),(2,'two')])
    submit = SubmitField("Отправить")
    def __init__(self, *args, **kwargs):
        self.name_maillist.choices = [(1,'один'),(2,'два')] 
        

        


"""
class UserDetails(Form):
    group_id = SelectField(u'Group', coerce=int)

def edit_user(request, id):
    user = User.query.get(id)
    form = UserDetails(request.POST, obj=user)
    form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
"""

# END классы форм