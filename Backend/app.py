from flask import Flask, render_template, request, redirect, url_for, session, jsonify,make_response
from flask_restful import Api
from API import Userapi, Book_section,Login,Book,Book_image
from Database.models import db, User
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager,get_jwt_identity
from flask_cors import CORS

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
api.add_resource(Book_image.Book_Image_api, '/Api/Book/<int:book_id>/image', methods=['GET', 'POST', 'PUT'])

app.add_url_rule('/login', 'login', Login.login, methods=['POST'])
app.add_url_rule('/Api/user/role', 'user_role', Login.get_user_role, methods=['GET'])

@jwt.user_identity_loader
def user_identity_lookup(user):
    return Login.user_identity_lookup(user)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        User.create_initial_admin()

    app.run(debug=True)
