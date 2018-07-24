from flask_sqlalchemy import SQLAlchemy
import config

from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

from models import *

def drop_all():
    db.drop_all()

def create_all():
    db.create_all()

def remove_session():
    db.session.remove()

if __name__ == "__main__":
    db.create_all()