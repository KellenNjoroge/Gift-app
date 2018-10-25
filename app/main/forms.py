from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write something about yourself', validators=[Required()])
    submit = SubmitField('Submit')


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required


class PlaceForm(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Title"})
    place_data = TextAreaField('New Place', )
    photo_url = StringField('Photo URL', render_kw={'placeholder': 'Photo URL'})
    location_url = StringField('Location URL', render_kw={'placeholder': 'Location URL'})
    post = SubmitField('Post place')


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[Required()], render_kw={"placeholder": "Name"})
    email = StringField('Email', validators=[Required()], render_kw={"placeholder": "Email"})
    comment_data = TextAreaField('Enter Comment', validators=[Required()], render_kw={"placeholder": "Comment"})
    post = SubmitField('Post Comment')


class EmailForm(FlaskForm):
    name = StringField('First Name', validators=[Required()], render_kw={"placeholder": "First Name"})
    email = StringField('Email', validators=[Required()], render_kw={"placeholder": "Email"})
    subscribe = SubmitField('Subscribe')
