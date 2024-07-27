from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Database.models import db, UserLog
from flask import jsonify, make_response
from datetime import datetime, timedelta
from API.Login import admin_required
from Database.cache import cache

log_fields = {
    'log_id': fields.Integer,
    'user_id': fields.Integer,
    'book_id': fields.Integer,
    'borrow_date': fields.DateTime,
    'return_date': fields.DateTime,
    'approved': fields.Integer,
}

class UserLogAPI(Resource):
    @jwt_required()
    @cache.cached()
    @marshal_with(log_fields)
    def get(self, log_id=None):
        user_id = get_jwt_identity()['user_id']
        admin = get_jwt_identity()['role']
        if log_id:
            log = UserLog.query.get(log_id)
            if log:
                return log
            else:
                return make_response(jsonify({'message': 'Log not found'}), 404)
        if admin == 'admin':
            logs = UserLog.query.all()
            return logs
        else:
            logs = UserLog.query.filter_by(user_id=user_id).all()
            return logs

    @jwt_required()
    def post(self):
        log_parser = reqparse.RequestParser()
        log_parser.add_argument('book_id', type=int, required=True, help='ID of the book')
        log_parser.add_argument('borrow_duration', type=int, required=True, help='Borrow duration in months')
        args = log_parser.parse_args()
        user_id = get_jwt_identity()['user_id']
        if args['borrow_duration']<28:
            return_date=datetime.utcnow() + timedelta(minutes=args['borrow_duration'])
        else:
            return_date=datetime.utcnow() + timedelta(days=args['borrow_duration'])
        logs = UserLog.query.filter_by(user_id=user_id).all()
        sum=0
        for log in logs:
            if log.approved >= 0:
                sum+=1
        if sum >= 5:
            return make_response(jsonify({'message': 'Cannot borrow more than 5 books.'}), 409)
        # Create a new log entry
        new_log = UserLog(
            user_id=user_id,
            book_id=args['book_id'],
            borrow_date=datetime.utcnow(),
            return_date=return_date,
            approved=0
        )
        
        db.session.add(new_log)
        db.session.commit()
        cache.clear()
        
        return make_response(jsonify({'message': 'Request submitted. Waiting for admin approval.'}), 201)

    @admin_required
    @marshal_with(log_fields)
    def put(self, log_id):
        log_parser = reqparse.RequestParser()
        log_parser.add_argument('approval', type=int, required=True, help='Approval of the request')
        args = log_parser.parse_args()
        
        approval = args['approval']

        log = UserLog.query.get(log_id)
        if not log:
            return make_response(jsonify({'message': 'Log not found'}), 404)
        
        # Update the log details
        log.approved = approval
        
        db.session.commit()
        cache.clear()
        return log

    @admin_required
    def delete(self, log_id):
        log = UserLog.query.get(log_id)
        if log:
            db.session.delete(log)
            db.session.commit()
            cache.clear()
            return make_response(jsonify({'message': 'Log deleted successfully'}), 204)
        else:
            return make_response(jsonify({'message': 'Log not found'}), 404)
