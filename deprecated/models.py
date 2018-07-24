from database import db
from datetime import datetime
from flask import url_for


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120))

    def __init__(self, first_name, user_id):
        self.first_name = first_name
        self.user_id = user_id

    def __repr__(self):
        return '<User name %r>' % self.first_name

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    likes = db.Column(db.String(120))
    dislikes = db.Column(db.String(120))
    profession = db.Column(db.String(120))
    birthday = db.Column(db.DateTime)
    location = db.Column(db.String(120))

    def __init__(self, title, text, pub_date=None, slug=None):
        self.title = title
        self.text = text
        self.slug = (slug or title).replace(' ', '_')
        self.pub_date = (pub_date or datetime.utcnow())

    def __repr__(self):
        return self.title

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    name = db.Column(db.String(120))

class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    condition = db.Column(db.String(120))
    feeling = db.Column(db.String(120))
    sentiment = db.Column(db.Float)