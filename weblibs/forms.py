from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Email, DataRequired, Length, EqualTo
from weblibs.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please enter another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please enter another one.')

class DeviceAddForm(FlaskForm):
    ieee_addr = StringField('IEEE Address', [DataRequired()])
    add = SubmitField('Add')
    remove = SubmitField('Remove')

class BrokerChangeForm(FlaskForm):
    addr = StringField('IP', [DataRequired()])
    port = StringField('Port', [DataRequired()])
    password = StringField('Password')
    change = SubmitField('Change')

# class DomoticzChangeForm(FlaskForm):
#     addr = StringField('IP', [DataRequired()])
#     port = StringField('Port', [DataRequired()])
#     password = StringField('Password')
#     change = SubmitField('Change')