from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField, TextAreaField
from wtforms.validators import Required, Email, EqualTo, Length
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(), Email()])
    username = StringField('Enter your username', validators=[Required()])
    password = PasswordField('Password',
                             validators=[Required(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self, data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError("There is an account with that email")

    def validate_username(self, data_field):
        if User.query.filter_by(username=data_field.data).first():
            raise ValidationError('That username is taken')


class LoginForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResetPassword(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    submit = SubmitField('Reset Password')


class NewPassword(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    password_repeat = PasswordField('Repeat Password', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Change Password')
