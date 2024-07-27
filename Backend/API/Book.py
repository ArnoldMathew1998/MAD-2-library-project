from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Database.models import db, Book
from flask import jsonify, make_response,abort
from API.Login import admin_required
from Database.cache import cache

# Define request parser and fields for serialization
Book_parser = reqparse.RequestParser()
Book_parser.add_argument('image_path', type=str, help='Path to the book image')
Book_parser.add_argument('pdf_path', type=str, help='Path to the book PDF')
Book_parser.add_argument('book_name', type=str, required=True, help='Name of the book')
Book_parser.add_argument('author_name', type=str, required=True, help='Name of the author')
Book_parser.add_argument('date_issued', type=str, required=True, help='Date the book was issued')
Book_parser.add_argument('content', type=str, required=True, help='Content of the book')
Book_parser.add_argument('language', type=str, required=True, help='Language of the book')
Book_parser.add_argument('price', type=float, required=True, help='Price of the book')


Book_fields = {
    'book_id': fields.Integer,
    'image_path': fields.String,
    'pdf_path': fields.String,
    'book_name': fields.String,
    'author_name': fields.String,
    'date_issued': fields.String,
    'content': fields.String,
    'language': fields.String,
    'price': fields.Float,
    'sec_id': fields.Integer
}


class BookAPI(Resource):
    @jwt_required()
    @cache.cached()
    @marshal_with(Book_fields)
    def get(self, book_id=None, section_id=None):
        if book_id:
            book = Book.query.get(book_id)
            return book
        elif section_id:
            books = Book.query.filter_by(sec_id=section_id).all()
            return books
        else:
            books = Book.query.all()
            return books

    @admin_required
    def put(self, book_id):
        args = Book_parser.parse_args()
        book = Book.query.get(book_id)
        if book:
            book.image_path = args['image_path']
            book.pdf_path = args['pdf_path']
            book.book_name = args['book_name']
            book.author_name = args['author_name']
            book.date_issued = args['date_issued']
            book.content = args['content']
            book.language = args['language']
            book.price = args['price']
            db.session.commit()
            updated_book_data = {
                'book_id': book.book_id,
                'image_path': book.image_path,
                'pdf_path': book.pdf_path,
                'book_name': book.book_name,
                'author_name': book.author_name,
                'date_issued': book.date_issued,
                'content': book.content,
                'language': book.language,
                'price': book.price,
                'sec_id': book.sec_id
            }
            cache.clear()
            return updated_book_data
        else:
            return 

    @admin_required
    @marshal_with(Book_fields)
    def post(self,section_id):
        args = Book_parser.parse_args()
        new_book = Book(
            image_path=args['image_path'],
            pdf_path=args['pdf_path'],
            book_name=args['book_name'],
            author_name=args['author_name'],
            date_issued=args['date_issued'],
            content=args['content'],
            language=args['language'],
            price=args['price'],
            sec_id=section_id
        )
        if args['image_path']=='':
            new_book.image_path = "default.jpg"
        db.session.add(new_book)
        db.session.commit()
        cache.clear()
        return new_book

    @admin_required
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            cache.clear()
            return make_response(jsonify({'message': 'Book deleted successfully'}), 204)
        else:
            return make_response(jsonify({'message': 'Book not found'}), 404)
