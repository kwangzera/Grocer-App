from traceback import format_exc

from flask import Blueprint, redirect, request, url_for, escape

from ..extensions import db
from ..scraper import scrape

user = Blueprint("user", __name__)

@user.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))

NUM_DEFAULT = 25
@user.route("/startup")
def startup():
    try:
        db.create_all()
        num = request.args.get("num", NUM_DEFAULT)
        if num == "all":
            with open("grocer_app/food.csv") as f:
                num = len(f)
        scrape(
            int(num),
            "https://grocer-app-flask.herokuapp.com/items",
            "grocer_app/food.csv",
        )
    except Exception as e:
        if isinstance(e.args[0], dict):
            return e.args[0]
        return {"message": repr(e), "messageFull": format_exc().splitlines()}
    else:
        return redirect(url_for('static', filename='startup.html'))
