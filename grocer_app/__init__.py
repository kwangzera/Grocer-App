from flask import Flask

from . import convert, models, queries
from .config import Config
from .extensions import db
from .routes import rest, user

def create_app():
    app = Flask(__name__.split()[0])
    app.config.from_object(Config)

    db.init_app(app)
    # db.create_all()

    app.register_blueprint(rest.rest)
    app.register_blueprint(user.user)

    return app

