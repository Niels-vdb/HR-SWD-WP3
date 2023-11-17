from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import email_validator


class LoginForm(FlaskForm):
    id = StringField('Studentnummer of personeelsemail',
                     validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    input = StringField('Studentnummer of werkemail', validators=[DataRequired()])
    submit = SubmitField('Vraag nieuw wachtwoord aan')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    confirm_password = PasswordField('Herhaal Wachtwoord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Stel nieuw wachtwoord in')
