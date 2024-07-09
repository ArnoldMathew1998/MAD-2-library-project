from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import pytz
from Database.models import db, BookSection
from flask import jsonify, make_response,abort
from API.Login import admin_required
# Define request parser and fields for serialization
Book_section_parser = reqparse.RequestParser()
Book_section_parser.add_argument('sec_name', type=str, required=True, help='Name of the book section')
Book_section_parser.add_argument('description', type=str, required=True, help='Description of the book section')

Section_fields = {
    'sec_id': fields.Integer,
    'sec_name': fields.String,
    'description': fields.String,
    'date_created': fields.String
}

class BookSectionAPI(Resource):
    @jwt_required()
    @marshal_with(Section_fields)
    def get(self, sec_id=None):
        if sec_id:
            book_section = BookSection.query.get(sec_id)
            if book_section:
                return book_section
            else:
                abort(404)
        else:
            sections = BookSection.query.all()
            if sections:
                return sections
            else:
                abort(404)

    @admin_required
    def put(self, sec_id):
        args = Book_section_parser.parse_args()
        book_section = BookSection.query.get(sec_id)
        if book_section:
            book_section.sec_name = args['sec_name']
            book_section.description = args['description']
            db.session.commit()
            updated_section_data = {
                'sec_id': book_section.sec_id,
                'sec_name': book_section.sec_name,
                'description': book_section.description,
                'date_created': book_section.date_created.strftime('%Y-%m-%d %H:%M:%S')
            }
            return updated_section_data
        else:
            return make_response(jsonify({'message': 'Book section not found'}), 404)

    @admin_required
    def post(self):
        args = Book_section_parser.parse_args()
        ist = pytz.timezone('Asia/Kolkata')
        utc_now = datetime.utcnow()
        ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)
        new_book_section = BookSection(
            sec_name=args['sec_name'],
            description=args['description'],
            date_created=ist_now
        )
        db.session.add(new_book_section)
        db.session.commit()
        new_section_data = {
        'sec_id': new_book_section.sec_id,
        'sec_name': new_book_section.sec_name,
        'description': new_book_section.description,
        'date_created': new_book_section.date_created.strftime('%Y-%m-%d %H:%M:%S')}
        
        return new_section_data

    @admin_required
    def delete(self, sec_id):
        book_section = BookSection.query.get(sec_id)
        print(sec_id)
        if book_section:
            db.session.delete(book_section)
            db.session.commit()
            return make_response(jsonify({'message': 'Book section deleted successfully'}), 204)
        else:
            return make_response(jsonify({'message': 'Book section not found'}), 404)
