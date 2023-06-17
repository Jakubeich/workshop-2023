from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Inicializace aplikace
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Nastavení databáze
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.sqlite')

# Inicializace databáze
db = SQLAlchemy(app)

# Inicializace Marshmallow
ma = Marshmallow(app)

# Definice modelu Kniha
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    author = db.Column(db.String(120))

    def __init__(self, title, author):
        self.title = title
        self.author = author
        
    def get_all_books():
        books = Book.query.all()
        return books
      
    def add_book(_title, _author):
        new_book = Book(_title, _author)
        db.session.add(new_book)
        db.session.commit()
        return new_book
    
    def edit_book(_id, _title, _author):
        book_to_edit = Book.query.filter_by(id=_id).first()
        book_to_edit.title = _title
        book_to_edit.author = _author
        db.session.commit()
        return book_to_edit
      
    def delete_book(_id):
        book_to_delete = Book.query.filter_by(id=_id).first()
        db.session.delete(book_to_delete)
        db.session.commit()
        return book_to_delete
    
# Schema knihy
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

# Inicializace schematu
book_schema = BookSchema()
books_schema = BookSchema(many=True)

### Endpointy ###

# Endpoint pro zobrazení všech knih
@app.route('/')
def index():
  all_books = Book.get_all_books()
  return render_template('index.html', books=all_books)

# Endpoint pro vytvoření knihy
@app.route('/book', methods=['POST'])
def add_book():
    title = request.json['title']
    author = request.json['author']
    new_book = Book.add_book(title, author)
    return book_schema.jsonify(new_book)

# Endpoint pro aktualizaci knihy
@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    title = request.json['title']
    author = request.json['author']
    book = Book.edit_book(id, title, author)
    return book_schema.jsonify(book)

# Endpoint pro smazání knihy
@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.delete_book(id)
    return book_schema.jsonify(book)

# Spuštění serveru
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)