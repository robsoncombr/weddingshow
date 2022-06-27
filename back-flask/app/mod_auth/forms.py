from flask_wtf import Form  # , RecaptchaField

# python2.7
#from wtforms import TextField, PasswordField  # BooleanField
# python:latest - TextField is deprecated
from wtforms import StringField, PasswordField  # BooleanField
# python2.7
#from wtforms.validators import Required, Email, EqualTo
from wtforms.validators import DataRequired, Email, EqualTo
# Define the login form (WTForms)
class LoginForm(Form):
    email = StringField('Email Address', [Email(),
                                          DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
        DataRequired(message='Must provide a password. ;-)')])
