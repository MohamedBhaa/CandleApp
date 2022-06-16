from flask import Flask, request, jsonify, redirect, url_for, render_template, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from asr import Recognize
from tts import convert
from io import BytesIO


# Configurations
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
search = Search(db=db)
search.init_app(app)


# Database Models
from models import *


# Routes
# Books Routes
@app.route('/api/books/', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        # Extract Data From JSON
        book_title = request.json['title']
        book_author = request.json['author']
        book_cover = request.json['cover']

        book = Book(title=book_title, author=book_author, cover=book_cover)
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': 'Book Added Successfully!', 'status': 201})

    else:
        books_obj = Book.query.all()

        books = []
        for book in books_obj:
            book_dict = {'id': book.id, 'title': book.title, 'cover': book.cover, 'author': book.author, 'date_added': book.date_added}
            books.append(book_dict)
        
        return jsonify({'Books': books})


@app.route('/api/books/<int:book_id>/', methods=['GET', 'PUT', 'DELETE'])
def book(book_id):
    book = Book.query.filter_by(id=book_id)

    if request.method == 'GET':
        book = book.first()
        book_dict = {'id': book.id, 'title': book.title, 'cover': book.cover, 'author': book.author, 'date_added': book.date_added}
        return jsonify(book_dict)

    elif request.method == 'PUT':
        # Extract Data From JSON
        book_title = request.json['title']
        book_author = request.json['author']
        book_cover = request.json['cover']

        book_dict = {'title': book_title, 'author': book_author, 'cover': book_cover}
        book.update(book_dict)
        db.session.commit()
        return jsonify({'message': 'Book Metadata Updated Successfully!', 'status': 200})

    else:
        book.delete()
        db.session.commit()
        return jsonify({'message': 'Book Deleted Successfully!', 'status': 200})


@app.route('/api/books/content/<int:book_id>', methods=['GET', 'PUT'])
def edit_content(book_id):
    if request.method == 'PUT':
        # Extract Data From File
        book_content = request.files['content']

        Book.query.filter_by(id=book_id).update({'content': book_content.read()})
        db.session.commit()
        return jsonify({'message': 'Book Content Updated Successfully!', 'status': 200})

    else:
        book = Book.query.filter_by(id=book_id).first()
        pdf_name = book.title + '.pdf'
        return send_file(BytesIO(book.content), attachment_filename=pdf_name, as_attachment=True)


@app.route('/api/books/audio/<int:book_id>')
def audio_book(book_id):
    book = Book.query.filter_by(id=book_id).first()

    with open('file.pdf', 'wb') as pdf:
        pdf.write(book.content)

    convert("file.pdf")

    return send_file('audio.mp3', attachment_filename='audio.mp3', as_attachment=True)


@app.route('/api/books/search/<string:query>')
def book_search(query):
    search.create_index(Book)
    results = Book.query.msearch(query).all()

    books = []
    for result in results:
        book_dict = {'id': result.id, 'title': result.title, 'cover': result.cover, 'author': result.author}
        books.append(book_dict)
    
    return jsonify({'Books': books})


# Users Routes
@app.route('/api/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        # Extract Data From JSON
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        phone = request.json['phone']

        user = User(username=username, email=email, password=generate_password_hash(password), phone=phone)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User Added Successfully!', 'status': 201})

    else:
        users_obj = User.query.all()

        users = []
        for user in users_obj:
            user_dict = {'username': user.username, 'email': user.email, 'password': user.password,
                'date_joined': user.date_joined, 'phone': user.phone}
            users.append(user_dict)

        return jsonify({'Users': users})


@app.route('/api/users/<string:user_name>/', methods=['GET', 'PUT', 'DELETE'])
def user(user_name):
    user = User.query.filter_by(username=user_name)

    if request.method == 'GET':
        user = user.first()
        user_dict = {'username': user.username, 'email': user.email, 'password': user.password, 'phone': user.phone}
        return jsonify(user_dict)

    elif request.method == 'PUT':
        # Extract Data From JSON
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        phone = request.json['phone']

        user_dict = {'username': username, 'email': email, 'password': generate_password_hash(password), 'phone': phone}
        user.update(user_dict)
        db.session.commit()
        return jsonify({'message': 'User Updated Successfully!', 'status': 200})

    else:
        user.delete()
        db.session.commit()
        return jsonify({'message': 'User Deleted Successfully!', 'status': 200})


@app.route('/api/users/picture/<string:user_name>', methods=['GET', 'PUT'])
def edit_picture(user_name):
    user = User.query.filter_by(username=user_name).first()

    if request.method == 'PUT':
        # Extract Data From File
        picture = request.files['picture']

        User.query.filter_by(id=user_id).update({'picture': picture.read()})
        db.session.commit()
        return jsonify({'message': 'User Picture Updated Successfully!', 'status': 200})
    
    else:
        picture_name = str(user.username) + '.jpg'
        return send_file(BytesIO(user.picture), attachment_filename=picture_name, as_attachment=True)


@app.route('/api/users/validate/', methods=['POST'])
def check_user():
    # Extract Data From JSON
    username = request.json['username']
    password = request.json['password']
    
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            return jsonify({'user_valid': True, 'username': user.username, 'email': user.email})

    return jsonify({'user_valid': False, 'username': '', 'email': ''})


# Requests Routes
@app.route('/api/requests/', methods=['GET', 'POST'])
def requests():
    if request.method == 'POST':
        # Extract Data From JSON
        request_books = request.json['books_requested']
        request_user = request.json['user_id']

        user = User.query.filter_by(id=request_user).first()
        req = Request(books_requested=request_books, user=user)
        db.session.add(req)
        db.session.commit()
        return jsonify({'message': 'Request Added Successfully!', 'status': 201})

    else:
        requests_obj = Request.query.all()

        requests = []
        for req in requests_obj:
            req_dict = {'id': req.id, 'books_requested': req.books_requested, 'req_date': req.req_date, 'user_id': req.user_id}
            requests.append(req_dict)
        
        return jsonify({'Requests': requests})


@app.route('/api/requests/<int:req_id>', methods=['GET', 'PUT', 'DELETE'])
def requesting(req_id):
    req = Request.query.filter_by(id=req_id)

    if request.method == 'GET':
        req = req.first()
        req_dict = {'id': req.id, 'books_requested': req.books_requested, 'req_date': req.req_date, 'user_id': req.user_id}
        return jsonify({'request': req_dict})

    elif request.method == 'PUT':
        # Extract Data From JSON
        request_books = request.json['books_requested']
        request_user = request.json['user_id']

        req_dict = {'books_requested': request_books, 'user_id': request_user}
        req.update(req_dict)
        db.session.commit()
        return jsonify({'message': 'Request Updated Successfully!', 'status': 200})

    else:
        req.delete()
        db.session.commit()
        return jsonify({'message': 'Request Deleted Successfully!', 'status': 200})


@app.route('/api/transcriptions/', methods=['POST'])
def voice_search():
    # Extract Data From File
    audio = request.files['audio']

    audio.save('user_audio.wav')
    transcripts = Recognize('user_audio.wav')

    search.create_index(Book)
    results = Book.query.msearch(transcripts).all()

    books = []
    for result in results:
        book_dict = {'id': result.id, 'title': result.title, 'cover': result.cover, 'author': result.author}
        books.append(book_dict)
    
    return jsonify({'Books': books})


if __name__ == '__main__':
    app.run()