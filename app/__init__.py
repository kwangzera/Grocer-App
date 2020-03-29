# This is to make /app a package

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy  # off with that red underscore
# from flask_migrate import Migrate

app = Flask(__name__.split()[0])
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import this *after* cuz app has to be defined first
from . import convert, models, queries, routes

