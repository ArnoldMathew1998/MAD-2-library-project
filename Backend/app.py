from flask import Flask
from flask_restful import Api
from API import Userapi, Book_section, Login, Book, Feedback, Cart, Wishlist, User_log
from Database.models import db, User
from Database.cache import cache
from flask_cors import CORS
import redis
from datetime import timedelta
import flask_excel as excel
from celery import Celery
from celery.schedules import crontab


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Mad-2-project'
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)

# Configuration for Flask-Caching
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 3
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300


# Configuration for Celery

app.config['result_backend'] = 'redis'
app.config['redis_host'] = 'localhost'
app.config['redis_port'] = 6379
app.config['redis_db'] = 2
app.config['broker_url'] = 'redis://localhost:6379/1'
app.config['result_backend'] = 'redis://localhost:6379/2'
app.config['beat_schedule'] = {
    'Daily-Reminder': {
        'task': 'Jobs.Task.reminder_email',
        'schedule': timedelta(seconds=60)
    },
    'Monthly-Activity': {
        'task': 'Jobs.Task.monthly_activity_summary',
        'schedule': timedelta(seconds=240)
    },
    'Generate-Chart': {
        'task': 'Jobs.Task.generate_chart',
        'schedule': timedelta(seconds=180)
    }
}
app.config['timezone'] = 'UTC'
app.config['broker_connection_retry_on_startup']=True



db.init_app(app)
cache.init_app(app)
excel.init_excel(app)
Login.jwt.init_app(app)
api = Api(app)
CORS(app)


redis_connection = redis.StrictRedis(
            host=app.config['redis_host'],
            port=app.config['redis_port'],
            db=app.config['redis_db']
            )
app.redis = redis_connection


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url'],
        include=["Jobs.Task"]
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery_app = make_celery(app)



# Add resources to the API
api.add_resource(Userapi.UserAPI, '/Api/user', '/Api/user/<int:user_id>', '/Api/user/<string:Username>')
api.add_resource(Book_section.BookSectionAPI, '/Api/Section', '/Api/Section/<int:sec_id>')
api.add_resource(Book.BookAPI, '/Api/Book', '/Api/Book/<int:book_id>', '/Api/Section/<int:section_id>/Book')
api.add_resource(Feedback.FeedbackAPI, '/Api/Feedback', '/Api/Book/<int:book_id>/Feedback', '/Api/User/<int:user_id>/Feedback', '/Api/Feedback/<int:book_id>/<int:user_id>')
api.add_resource(Cart.CartAPI, '/Api/cart', '/Api/cart/<int:book_id>')
api.add_resource(Wishlist.WishlistAPI, '/Api/wishlist', '/Api/wishlist/<int:book_id>')
api.add_resource(User_log.UserLogAPI, '/Api/logs', '/Api/logs/<int:log_id>')

app.add_url_rule('/login', 'login', Login.login, methods=['POST'])
app.add_url_rule('/search', 'search', Login.search_books, methods=['GET'])
app.add_url_rule('/Order/Approve/<int:log_id>', 'Approve', Login.exipred, methods=['GET'])
app.add_url_rule('/logout', 'logout', Login.logout, methods=['POST'])
app.add_url_rule('/admin/dashboard', 'dashboard', Login.admin_dashboard, methods=['GET'])
app.add_url_rule('/search/section', 'search_section', Login.search_Sections, methods=['GET'])
app.add_url_rule('/search/section/book/<int:sec_id>', 'search_section_books', Login.search_section_books, methods=['GET'])
app.add_url_rule('/generate_report', 'generate_report', Login.generate_report, methods=['GET'])
app.add_url_rule('/generate_report/<task_id>', 'report_status', Login.get_report_status, methods=['GET'])
app.add_url_rule('/Api/file/upload', 'upload_file', Login.upload_file, methods=['POST'])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        User.create_initial_admin()
        
        
    app.run(debug=True)
