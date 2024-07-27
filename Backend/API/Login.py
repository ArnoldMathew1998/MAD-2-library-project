from flask import request, jsonify, make_response,abort,send_file
from Database.models import User, db, Book, UserLog, BookSection
from flask_jwt_extended import create_access_token, jwt_required, JWTManager,get_jwt_identity
from datetime import datetime, timedelta
from Jobs.Task import generate_csv,celery_app
from Database.cache import cache
import os
from werkzeug.utils import secure_filename

jwt = JWTManager()

@jwt.user_identity_loader
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


def search_books():
    query = request.args.get('query', '')

    if query:
        books = Book.query.filter(
            db.or_(
                Book.book_id.ilike(f'%{query}%'),
                Book.book_name.ilike(f'%{query}%'),
                Book.author_name.ilike(f'%{query}%'),
                Book.content.ilike(f'%{query}%')
            )
        ).all()
    else:
        books = Book.query.all()

    results = [
        {
            'book_id': book.book_id,
            'book_name': book.book_name,
            'author_name': book.author_name,
            'date_issued': book.date_issued,
            'content': book.content,
            'price': book.price
        }
        for book in books
    ]

    return jsonify(results)

@jwt_required()
def search_Sections():
    query = request.args.get('query', '')

    if query:
        Sections = BookSection.query.filter(
            db.or_(
                BookSection.sec_id.ilike(f'%{query}%'),
                BookSection.sec_name.ilike(f'%{query}%'),
                BookSection.description.ilike(f'%{query}%')
            )
        ).all()
    else:
        Sections = BookSection.query.all()
    results = [
    {
        'sec_id': Section.sec_id,
        'sec_name': Section.sec_name,
        'date_created': Section.date_created,
        'description': Section.description,
    }
    for Section in Sections
    ]
    return jsonify(results)

@jwt_required()
def search_section_books(sec_id):
    query = request.args.get('query', '')

    if query:
        books = Book.query.filter_by(sec_id=sec_id).filter(
            db.or_(
                Book.book_id.ilike(f'%{query}%'),
                Book.book_name.ilike(f'%{query}%'),
                Book.author_name.ilike(f'%{query}%'),
                Book.content.ilike(f'%{query}%')
            )
        ).all()
            
    else:
        books = Book.query.filter_by(sec_id=sec_id).all()
    
    results = [
        {
            'book_id': book.book_id,
            'book_name': book.book_name,
            'author_name': book.author_name,
            'date_issued': book.date_issued,
            'content': book.content,
            'sec_id': book.sec_id,
            'language': book.language,
            'price': book.price,
            'image_path': book.image_path,
            'pdf_path': book.pdf_path
        }
        for book in books
    ]

    return jsonify(results)

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        role = get_jwt_identity()['role']
        if role != 'admin':
            return make_response(jsonify({'message': 'Admin access required'}), 403)
        return fn(*args, **kwargs)
    return wrapper


def exipred(log_id):
    log = UserLog.query.get(log_id)
    if not log:
        return make_response(jsonify({'message': 'Log not found'}), 404)
    now = datetime.utcnow()
    if log.return_date <= now:
        log.approved = -2
        db.session.commit()
        return make_response(jsonify({'message': 'Log deleted successfully'}), 204)
    else:
        return make_response(jsonify({'message': 'Log not expired'}), 404)

@jwt_required()
def logout():
    return jsonify({'message': 'Logout successful'})


@admin_required
@cache.cached()
def admin_dashboard():
    user_logs = UserLog.query.all()
    total_revenue = sum(log.book.price for log in user_logs if log.approved == 1 or log.approved == -2)
    active_user_ids = db.session.query(UserLog.user_id).filter(UserLog.approved.in_([1, 0])).distinct().all()
    active_user_ids = [user_id[0] for user_id in active_user_ids]
    
    
    return jsonify({"total_revenue":total_revenue,"total_requests":len(user_logs),"active_users":len(active_user_ids)})


@admin_required
def generate_report():
    task = generate_csv.delay()
    return jsonify({"task_id":task.id})



def get_report_status(task_id):
    task = celery_app.AsyncResult(task_id)
    if task.ready:
        filename = task.result
        return send_file(filename, as_attachment=True)
    return jsonify({"status":task.ready}), 202


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../../Frontend/src/assets/book_image")

def upload_file():
        if 'file' not in request.files:
            print("No file part in the request")
            return make_response(jsonify({'error': 'No file part in the request'}), 400)

        file = request.files['file']
        if file.filename == '':
            print("No file selected for uploading")
            return make_response(jsonify({'error': 'No file selected for uploading'}), 400)

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            url = f"{filename}"
            return make_response(jsonify({'path': url}), 200)

        return make_response(jsonify({'error': 'Something went wrong'}), 500)
