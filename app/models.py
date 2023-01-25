from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique = True)
    email = db.Column(db.String(150), nullable=False, unique = True)
    password = db.Column(db.String, nullable=False)
    post = db.relationship("Post", backref='author', lazy = True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    # add to database and commit
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False, default=datetime.utcnow())
    caption = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, image_url, user_id):
        self.title = title
        self.image_url = image_url
        self.user_id = user_id
    pass

