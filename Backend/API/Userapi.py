from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Database.models import db, User
from flask import jsonify, make_response

user_output = {
    'user_id': fields.Integer,
    'profile_photo': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'mail_id': fields.String,
    'role': fields.String
}

class UserAPI(Resource):
    @marshal_with(user_output)
    @jwt_required()
    def get(self, user_id=None, mail_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user
            else:
                return {'message': 'User not found'}, 404
        elif mail_id:
            user = User.query.filter_by(mail_id=mail_id).first()
            if user:
                return user
            else:
                return {'message': 'User not found'}, 404
        
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
            return {'message': 'Unauthorized: You can only update your own profile or you must be an admin'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=False, help='First name of the user')
        parser.add_argument('last_name', type=str, required=False, help='Last name of the user')
        parser.add_argument('profile_photo', type=str, required=False, help='Base64-encoded image data')
        parser.add_argument('mail_id', type=str, required=False, help='Mail ID of the user')
        parser.add_argument('password', type=str, required=False, help='Password of the user')
        parser.add_argument('role', type=str, required=False, help='Role of the user')
        args = parser.parse_args()

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        if args['role'] and current_user_role == 'admin':
            user.role = args['role']
        elif args['role']:
            return {'message': 'Unauthorized: Only admin can change roles'}, 401

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

        db.session.commit()
        return {'message': 'User updated successfully'}, 200

    @jwt_required()
    def delete(self, user_id):
        current_user = get_jwt_identity()
        current_user_id = current_user['user_id']
        current_user_role = current_user['role']
        
        if current_user_id != user_id and current_user_role != 'admin':
            return {'message': 'Unauthorized: You can only delete your own profile or you must be an admin'}, 401

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 204
