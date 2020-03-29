from flask import Blueprint, redirect, request, url_for

user = Blueprint("user", __name__)

@user.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))

NUM_DEFAULT = 25
@user.route("/startup")
def startup():
    try:
        from ..extensions import db
        from ..scraper import scrape
        db.create_all()
        scrape(
            request.args.get(num, NUM_DEFAULT),
            "https://grocer-app-flask.herokuapp.com/items",
            "food.csv",
        )
    except Exception as e:
        return f"Fatal Error: {repr(e)}"
    else:
        return redirect(url_for('static', filename='startup.html'))
