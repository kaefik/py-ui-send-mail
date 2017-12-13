from wtforms import Form, StringField, SubmitField, TextAreaField, PasswordField, validators

# классы форм
class CreateEmailTemplateForm(Form):
    subjectmail = StringField("Тема письма: ", [validators.Length(min=5, max=100)])
    messagemail = TextAreaField("Содержание письма: ", [validators.Length(min=5)])    
    submit = SubmitField("Сохранить")


# END классы форм