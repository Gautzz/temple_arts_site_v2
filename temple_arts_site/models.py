from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default="General")
    author_name = db.Column(db.String(120), default="Temple Committee")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TempleEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temple_name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    gregorian_date = db.Column(db.Date, nullable=False)
    malayalam_month = db.Column(db.String(50))
    malayalam_day = db.Column(db.Integer)
    nakshatram = db.Column(db.String(50))
    location = db.Column(db.String(200))
    author_name = db.Column(db.String(120), default="Temple Committee")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
