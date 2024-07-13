from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Database.models import db, Feedback
from flask import jsonify, make_response, abort
from datetime import datetime
from API.Login import admin_required

# Define request parser and fields for serialization
Feedback_parser = reqparse.RequestParser()
Feedback_parser.add_argument('user_id', type=int,  help='ID of the user')
Feedback_parser.add_argument('book_id', type=int,  help='ID of the book')
Feedback_parser.add_argument('feedback_text', type=str, required=True, help='Text of the feedback')
Feedback_parser.add_argument('feedback_rating', type=int, required=True, help='Rating of the feedback')

Feedback_fields = {
    'user_id': fields.Integer,
    'book_id': fields.Integer,
    'feedback_text': fields.String,
    'feedback_date': fields.DateTime,
    'feedback_rating': fields.Integer
}

class FeedbackAPI(Resource):
    @jwt_required()
    @marshal_with(Feedback_fields)
    def get(self, book_id=None, user_id=None):
        if book_id:
            feedbacks = Feedback.query.filter_by(book_id=book_id).all()
            return feedbacks
        elif user_id:
            feedbacks = Feedback.query.filter_by(user_id=user_id).all()
            return feedbacks  
        else:
            feedbacks = Feedback.query.all()
            return feedbacks

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        args = Feedback_parser.parse_args()
        if args['feedback_rating'] < 1 or args['feedback_rating'] > 5:
            return make_response(jsonify({'message': 'Rating must be between 1 and 5'}), 400)
               
        
        new_feedback = Feedback(
            user_id=current_user['user_id'],
            book_id=args['book_id'],
            feedback_text=args['feedback_text'],
            feedback_date=datetime.utcnow(),
            feedback_rating=args['feedback_rating']
        )
        db.session.add(new_feedback)
        db.session.commit()
       
       
        new_feedback_data = {
            'user_id': new_feedback.user_id,
            'book_id': new_feedback.book_id,
            'feedback_text': new_feedback.feedback_text,
            'feedback_date': new_feedback.feedback_date,
            'feedback_rating': new_feedback.feedback_rating
        }
        return jsonify(new_feedback_data)

    @jwt_required()
    def put(self,book_id):
        
        current_user = get_jwt_identity()
        feedback = Feedback.query.filter_by(user_id = current_user['user_id'], book_id = book_id).first()
        
        if not feedback:
            return make_response(jsonify({'message': 'Feedback not found'}), 404)
        
        
        args = Feedback_parser.parse_args()
        if args['feedback_rating'] < 1 or args['feedback_rating'] > 5:
            return make_response(jsonify({'message': 'Rating must be between 1 and 5'}), 400)
        
        feedback.feedback_text = args['feedback_text']
        feedback.feedback_rating = args['feedback_rating']
        
        db.session.commit()
        
        updated_feedback_data = {
            'user_id': feedback.user_id,
            'book_id': feedback.book_id,
            'feedback_text': feedback.feedback_text,
            'feedback_date': feedback.feedback_date,
            'feedback_rating': feedback.feedback_rating
        }
        
        return jsonify(updated_feedback_data)

    @jwt_required()
    def delete(self, book_id):
        current_user = get_jwt_identity()
        feedback = Feedback.query.filter_by(user_id = current_user['user_id'], book_id = book_id).first()
                
        if feedback:
            db.session.delete(feedback)
            db.session.commit()
            
            return jsonify({'message': 'Feedback deleted successfully'})
        else:
            return make_response(jsonify({'message': 'Feedback not found'}), 404)



