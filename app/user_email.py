from flask_mail import Message
from . import mail
from flask import render_template
import os
subject_pref = 'gift-app'
sender_email = 'muthonkel@gmail.com'


def mail_message(subject, template, to, **kwargs):

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body = render_template(template + ".txt", **kwargs)
    email.html = render_template(template + ".html", **kwargs)
    mail.send(email)

def send_reset_email(user):
    token = user.get_reset_password_token()
    mail_message('Reset Password', sender=os.environ.get['MAIL_USERNAME'], recipients=[user.email],
               text_body=render_template('auth/reset_password.txt', user=user, token=token),
               html_body=render_template('auth/reset_password.html', user=user, token=token))
