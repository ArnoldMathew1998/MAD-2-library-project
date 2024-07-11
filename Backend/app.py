from flask import Flask, render_template, request, redirect, url_for, session, jsonify,make_response
from flask_restful import Api
from API import Userapi, Book_section,Login,Book
from Database.models import db, User
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager,get_jwt_identity
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Mad-2-project'
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!



db.init_app(app)
jwt = JWTManager(app)
api = Api(app)
CORS(app)

scheduler = BackgroundScheduler()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "C:/Users/rkoma/Mad-2 LIB Mangment/Frontend/src/assets/book_image")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


""" if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
 """

@app.route('/Api/Book/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return make_response(jsonify({'error': 'No file part in the request'}), 400)

    file = request.files['file']
    if file.filename == '':
        return make_response(jsonify({'error': 'No file selected for uploading'}), 400)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        url = f"{filename}"
        return make_response(jsonify({'path': url}), 200)

    return make_response(jsonify({'error': 'Something went wrong'}), 500)

# def delete_User_log_auto():
#     user_log_api = 'http://127.0.0.1:5000/Api/user/logs/'
#     response = requests.delete(user_log_api)
#     if response.status_code == 200:
#         print("User auto delete")
#     return

# scheduler.add_job(delete_User_log_auto, 'interval', seconds=60)
# scheduler.start()

# Add resources to the API
api.add_resource(Userapi.UserAPI, '/Api/user', '/Api/user/<int:user_id>','/Api/user/<string:Username>')
api.add_resource(Book_section.BookSectionAPI, '/Api/Section', '/Api/Section/<int:sec_id>')
api.add_resource(Book.BookAPI, '/Api/Book', '/Api/Book/<int:book_id>','/Api/Section/<int:section_id>/Book')


app.add_url_rule('/login', 'login', Login.login, methods=['POST'])


@jwt.user_identity_loader
def user_identity_lookup(user):
    return Login.user_identity_lookup(user)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        User.create_initial_admin()
    app.run(debug=True)
