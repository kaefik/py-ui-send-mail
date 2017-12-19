from wtforms import Form, StringField, SubmitField, TextAreaField, PasswordField, validators

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


# END классы форм