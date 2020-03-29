# Configuration file for database

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Disable aa featur of FLask-SQLAlchemy that is not needed
    # -> feature to signal application every time a change is 
    # about to be made in teh database
