from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Database.models import db, Wishlist
from flask import jsonify, make_response


# Define request parser and fields for serialization
Wishlist_parser = reqparse.RequestParser()
Wishlist_parser.add_argument('book_id', type=int, required=True, help='ID of the book')

Wishlist_fields = {
    'user_id': fields.Integer,
    'book_id': fields.Integer
}

class WishlistAPI(Resource):
    @jwt_required()
    @marshal_with(Wishlist_fields)
    def get(self):
        user_id = get_jwt_identity()['user_id']
        wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
        return wishlist_items

    @jwt_required()
    @marshal_with(Wishlist_fields)
    def post(self):
        user_id = get_jwt_identity()['user_id']
        args = Wishlist_parser.parse_args()
        new_wishlist_item = Wishlist(user_id=user_id, book_id=args['book_id'])
        db.session.add(new_wishlist_item)
        db.session.commit()
        return new_wishlist_item

    @jwt_required()
    def delete(self, book_id):
        user_id = get_jwt_identity()['user_id']
        wishlist_item = Wishlist.query.filter_by(book_id=book_id, user_id=user_id).first()
        if wishlist_item:
            db.session.delete(wishlist_item)
            db.session.commit()
            return make_response(jsonify({'message': 'Wishlist item deleted successfully'}), 200)
        else:
            return make_response(jsonify({'message': 'Wishlist item not found'}), 404)
