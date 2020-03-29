from flask import Blueprint, redirect, request, url_for

from .extensions import db
user = Blueprint("user", __name__)

@user.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))

@user.route("/startup")
def startup():
    db.create_all()
    return redirect(url_for('static', filename='startup.html'))
