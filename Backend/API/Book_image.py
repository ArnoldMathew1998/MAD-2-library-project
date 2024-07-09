from flask_restful import Resource, reqparse
from Database.models import db,Book_Image
from flask import jsonify, make_response,abort
from API.Login import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import base64

image_parser = reqparse.RequestParser()
image_parser.add_argument('image_data', type=str, required=True, help='Base64-encoded image data')


class Book_Image_api(Resource):
    @jwt_required
    def get(self, book_id):
        image = Book_Image.query.get(book_id)
        if image:
            return image.image_data
        else:
            abort(404, message="Book_Image not found")
    @admin_required
    def post(self, book_id):
        args = image_parser.parse_args()
        
        image_data = args['image_data']
        pic=image_data
        image_data_base64 = base64.b64encode(pic.read()).decode('utf-8')
        new_image = Book_Image(image_data=image_data, book_id=book_id)
        db.session.add(new_image)
        db.session.commit()

        return make_response(jsonify({'message': 'Book_Image uploaded successfully'}), 201)
    @admin_required
    def put(self, book_id):
        args = image_parser.parse_args()
        image = Book_Image.query.get(book_id)
        image_data = args['image_data']

        if image:
            image.image_data = image_data
        db.session.commit()
        return make_response(jsonify({'message': 'Book_Image uploaded successfully'}), 201)
    
    