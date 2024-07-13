from flask import request, jsonify, make_response,abort
from Database.models import User
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager,get_jwt_identity

def user_identity_lookup(user):
    if isinstance(user, User):
        return {
            'user_id': user.user_id,
            'role': user.role
        }
    elif isinstance(user, dict):
        return {
            'user_id': user.get('user_id'),
            'role': user.get('role')
        }
    return user
   

def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(mail_id=username).one_or_none()
    if not user or not user.check_password(password):
        abort(401)

    access_token = create_access_token(identity=user_identity_lookup(user))
    user={
        "user_id":user.user_id,
        "role":user.role,
        "access_token":access_token,
        "username":user.mail_id,
        "name":user.first_name+" "+user.last_name,
        "profile_photo":user.profile_photo

    }
    return user

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        role = get_jwt_identity()['role']
        if role != 'admin':
            return make_response(jsonify({'message': 'Admin access required'}), 403)
        return fn(*args, **kwargs)
    return wrapper



