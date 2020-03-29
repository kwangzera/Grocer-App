from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__.split()[0])
app.config.from_object(Config)
db = SQLAlchemy(app)
db.create_all()  # idempotent

from . import convert, models, queries, routes
