from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Database.models import db, Cart
from flask import jsonify, make_response
from Database.cache import cache

# Define request parser and fields for serialization
Cart_parser = reqparse.RequestParser()
Cart_parser.add_argument('book_id', type=int, required=True, help='ID of the book')

Cart_fields = {
    'user_id': fields.Integer,
    'book_id': fields.Integer
}

class CartAPI(Resource):
    @jwt_required()
    @marshal_with(Cart_fields)
    def get(self):
        user_id = get_jwt_identity()['user_id']
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        return cart_items

    @jwt_required()
    @marshal_with(Cart_fields)
    def post(self):
        user_id = get_jwt_identity()['user_id']
        args = Cart_parser.parse_args()
        new_cart_item = Cart(user_id=user_id, book_id=args['book_id'])
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item

    @jwt_required()
    def delete(self, book_id):
        user_id = get_jwt_identity()['user_id']
        cart_item = Cart.query.filter_by(book_id=book_id, user_id=user_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return make_response(jsonify({'message': 'Cart item deleted successfully'}), 200)
        else:
            return make_response(jsonify({'message': 'Cart item not found'}), 404)
