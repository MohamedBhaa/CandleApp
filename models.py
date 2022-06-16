from datetime import datetime
from app import db


book_request = db.Table('book_request',
    db.Column('reqID', db.Integer, db.ForeignKey('request.id'), primary_key=True),
    db.Column('bookID', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('date_placed', db.DateTime, default=datetime.now))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.now)
    phone = db.Column(db.String(20), default=None)
    picture = db.Column(db.LargeBinary)
    admin = db.Column(db.Boolean, default=False)
    requests = db.relationship('Request', backref='user')


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    books_requested = db.Column(db.Text, nullable=False)
    req_date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String, default='Waiting')
    book_id = db.relationship('Book', secondary=book_request, backref='request')


class Book(db.Model):
    __searchable__ = ['title', 'author']
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    cover = db.Column(db.String(200), default='https://islandpress.org/sites/default/files/default_book_cover_2015.jpg')
    rating = db.Column(db.String(5))
    content = db.Column(db.LargeBinary)
    date_added = db.Column(db.DateTime, default=datetime.now)