from flask import render_template, redirect, url_for, abort, request
from . import main
from ..models import User
from flask_login import login_required, current_user
from .. import db, photos

@main.route('/')
def index():
    """
    root page function that returns the index page and its data
    """
    title = "Welcome "

    return render_template("index.html", title=title)
