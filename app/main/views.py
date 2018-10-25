from flask import render_template, redirect, url_for, flash, abort, request
from . import main
from ..models import User, Place, Comment
from flask_login import login_required, current_user
from .. import db, photos
from .forms import UpdateProfile, PlaceForm, CommentForm
import requests
import os
import imghdr
from datetime import datetime
from time import time, sleep
import markdown2

key = os.environ.get('API_KEY')

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo"


@main.route('/')
def index():
    """
    root page function that returns the index page and its data
    """
    title = "Welcome "

    return render_template("index.html", title=title)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    update_form = UpdateProfile()

    if update_form.validate_on_submit():
        user.bio = update_form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username, id_user=user.id))
    title = 'Update Bio'
    return render_template('profile/update.html', form=update_form, title=title)


@main.route('/user/<uname>/update/userpic', methods=['POST'])
@login_required
def update_userpic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname, id_user=current_user.id))


@main.route('/place/<int:id>', methods=['GET', 'POST'])
def place(id):
    get_place = Place.query.get(id)
    get_place_comments = Comment.get_place_comments(id)

    if get_place is None:
        abort(404)

    place_format = markdown2.markdown(get_place.place_content, extras=["code-friendly", "fenced-code-blocks"])

    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        user_name = comment_form.name.data
        user_email = comment_form.email.data
        user_comment = comment_form.comment_data.data

        new_comment = Comment(name=user_name, email=user_email, comment_content=user_comment,
                              date_comment=datetime.now(), place_id=id)
        new_comment.save_comment()

        return redirect(url_for('main.place', id=id))

    get_comments = Comment.get_place_comments(id)

    return render_template('place.html', place_format=place_format, get_place=get_place, title="New Gift shop",
                           comment_form=comment_form, get_comments=get_comments, comments_count=len(get_place_comments))


@main.route('/create_place', methods=['GET', 'POST'])
@login_required
def create_place():
    place_form = PlaceForm()

    if place_form.validate_on_submit():
        place_title = place_form.title.data
        place = place_form.place_data.data
        url = place_form.photo_url.data
        url_second = place_form.location_url.data

        new_place = Place(title=place_title, place_content=place, date_posted=datetime.now(), photo_url=url, location_url=url_second)
        new_place.save_place()

        # send_places(new_place)
        # return redirect(url_for('main.place', id=new_place.id))

    return render_template('new_place.html', title='New Place', place_form=place_form)


@main.route('/place/<int:id>/update/pic', methods=['POST'])
@login_required
def update_pic(id):
    place = Place.get_single_place(id)
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        place.place_pic = path
        # user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.place', id=id))


@main.route('/place/<int:id>/<int:id_comment>/delete_comment')
@login_required
def delete_comment(id, id_comment):
    comment = Comment.get_single_comment(id, id_comment)

    db.session.delete(comment)
    db.session.commit()

    flash('Comment has been deleted')

    return redirect(url_for('main.place', id=id))


@main.route('/index/<int:id>/delete_place')
@login_required
def delete_place(id):
    place = Place.get_single_place(id)

    db.session.delete(place)
    db.session.commit()

    flash('Place has been deleted')

    return redirect(url_for('main.index'))


@main.route("/map_retrieve", methods=["GET"])
def retrieve():
    return render_template('places.html')


@main.route("/sendRequest/<string:query>")
def results(query):
    search_payload = {"key": key, "query": query}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()

    photo_id = search_json["results"][0]["photos"][0]["photo_reference"]

    photo_payload = {"key": key, "maxwidth": 500, "maxwidth": 500, "photoreference": photo_id}
    photo_request = requests.get(photos_url, params=photo_payload)

    photo_type = imghdr.what("", photo_request.content)
    photo_name = "static/" + query + "." + photo_type

    with open(photo_name, "wb") as photo:
        photo.write(photo_request.content)

    image = '<img src=' + photo_name + '>'
    return image

    return render_template('places.html', image=image)
