from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Database.models import db, User
from flask import jsonify, make_response
from Database.cache import cache
user_output = {
    'user_id': fields.Integer,
    'profile_photo': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'mail_id': fields.String,
    'role': fields.String
}

class UserAPI(Resource):
    @jwt_required()
    @cache.cached()
    @marshal_with(user_output)
    def get(self, user_id=None, mail_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user
            else:
                return make_response(jsonify({'message': 'User not found'}), 404)
        elif mail_id:
            user = User.query.filter_by(mail_id=mail_id).first()
            if user:
                return user
            else:
                return make_response(jsonify({'message': 'User not found'}), 404)
        
        else:
            users = User.query.all()
            return users

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True, help='First name of the user')
        parser.add_argument('last_name', type=str, required=False, help='Last name of the user')
        parser.add_argument('mail_id', type=str, required=True, help='Mail ID of the user')
        parser.add_argument('password', type=str, required=True, help='Password of the user')
        args = parser.parse_args()

        existing_user = User.query.filter_by(mail_id=args['mail_id']).first()
        if existing_user:
            return make_response(jsonify({'message': 'User with this email already exists'}), 409)

        new_user = User(
            first_name=args['first_name'],
            last_name=args['last_name'],
            mail_id=args['mail_id'],
            password=args['password']
        )

        db.session.add(new_user)
        db.session.commit()
        cache.clear()

        access_token = create_access_token(identity=new_user.get_jwt_identity())
        user={
        "user_id":new_user.user_id,
        "role":new_user.role,
        "access_token":access_token,
        "username":new_user.mail_id,
        "name":new_user.first_name+" "+new_user.last_name,
        "profile_photo":new_user.profile_photo

    }
        
        return user

    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        current_user_id = current_user['user_id']
        current_user_role = current_user['role']
        
        if current_user_id != user_id and current_user_role != 'admin':
            return make_response(jsonify({'message': 'Unauthorized: You can only update your own profile or you must be an admin'}), 401)
        
        
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=False, help='First name of the user')
        parser.add_argument('last_name', type=str, required=False, help='Last name of the user')
        parser.add_argument('profile_photo', type=str, required=False, help='Base64-encoded image data')
        parser.add_argument('profile_photo_url', type=str, required=False, help='confirm to delete photo')
        parser.add_argument('mail_id', type=str, required=False, help='Mail ID of the user')
        parser.add_argument('password', type=str, required=False, help='Password of the user')
        parser.add_argument('currentPassword', type=str, required=True, help='Current Password of the user')
        parser.add_argument('role', type=str, required=False, help='Role of the user')
        args = parser.parse_args()
        
        user = User.query.get(user_id)
        password = args['currentPassword']
        
        if not user.check_password(password):
            return make_response(jsonify({'message': 'Unauthorized: You can only update your own profile'}), 401)
        
        
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        if args['role'] and current_user_role == 'admin':
            user.role = args['role']
        
        if args['first_name']:
            user.first_name = args['first_name']
        if args['last_name']:
            user.last_name = args['last_name']
        if args['mail_id']:
            user.mail_id = args['mail_id']
        if args['password']:
            user.password = args['password']
        if args['profile_photo']:
            user.profile_photo = args['profile_photo']
        if args['profile_photo_url']=="delete":
            user.profile_photo = None
        db.session.commit()
        cache.clear()
        return make_response(jsonify({'message': 'User updated successfully'}), 200)

    @jwt_required()
    def delete(self, user_id):
        current_user = get_jwt_identity()
        current_user_id = current_user['user_id']
        current_user_role = current_user['role']
    
        if current_user_id != user_id and current_user_role != 'admin':
            return make_response(jsonify({'message': 'Unauthorized: You can only delete your own profile or you must be an admin'}), 401)
        
        parser = reqparse.RequestParser()
        parser.add_argument('currentPassword', type=str, required=True, help='Current Password of the user')
        args = parser.parse_args()

        user = User.query.get(user_id)
        
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)
        
        password = args['currentPassword']
        if not user.check_password(password):
            return make_response(jsonify({'message': 'Unauthorized: Incorrect password'}), 401)
        
        db.session.delete(user)
        db.session.commit()
        cache.clear()
        return make_response(jsonify({'message': 'User deleted successfully'}), 200)