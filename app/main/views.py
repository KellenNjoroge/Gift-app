from flask import render_template, redirect, url_for, abort, request
from . import main
from ..models import User
from flask_login import login_required, current_user
from .. import db, photos
import requests
import os
import imghdr

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

    image='<img src=' + photo_name + '>'
    return image

    return render_template('places.html', image=image)

# @main.route("/get_directions/<string:query>")
# def directions(query):
#
