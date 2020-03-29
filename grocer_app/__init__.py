from flask import Flask
from config import Config

from . import convert, models, queries
from .extensions import db
from .routes import rest, user

def create_app():
    app = Flase(__name__.split()[0])
    app.config.from_object(Config)
    
    db.init_app(app)

    app.register_blueprint(rest.rest)
    app.register_blueprint(user.user)

    return app

