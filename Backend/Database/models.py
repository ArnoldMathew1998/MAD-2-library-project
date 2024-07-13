from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String)
    pdf_path = db.Column(db.String)
    book_name = db.Column(db.String, nullable=False)
    author_name = db.Column(db.String, nullable=False)
    date_issued = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sec_id = db.Column(db.Integer, db.ForeignKey('book_section.sec_id', ondelete='CASCADE'), nullable=False)
    feedbacks = db.relationship('Feedback', backref='book', cascade='all, delete-orphan', lazy=True)
    """ user_logs = db.relationship('UserLog', backref='book', cascade='all, delete-orphan', lazy=True)
    cart = db.relationship('Cart', backref='book', cascade='all, delete-orphan', lazy=True)
    wishlist = db.relationship('Wishlist', backref='book', cascade='all, delete-orphan', lazy=True) """


class UserLog(db.Model):
    __tablename__ = 'user_log'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id', ondelete='CASCADE'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id', ondelete='CASCADE'), nullable=False)

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id', ondelete='CASCADE'), nullable=False)

class BookSection(db.Model):
    __tablename__ = 'book_section'
    sec_id = db.Column(db.Integer, primary_key=True)
    sec_name = db.Column(db.String, unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String, nullable=False)
    books = db.relationship('Book', backref='book_section', cascade='all, delete-orphan', lazy=True)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    profile_photo = db.Column(db.Text)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    mail_id = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='user')
    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete-orphan', lazy=True)
    """ user_logs = db.relationship('UserLog', backref='user', cascade='all, delete-orphan', lazy=True)
    cart = db.relationship('Cart', backref='user', cascade='all, delete-orphan', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', cascade='all, delete-orphan', lazy=True) """

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod 
    def create_initial_admin():
        if User.query.filter_by(role='admin').count() == 0:
            initial_admin = User(
                first_name='Admin',
                last_name='Library',
                mail_id='admin@example.com',
                password='password',  # Replace with actual initial admin password
                role='admin'
            )
            db.session.add(initial_admin)
            db.session.commit()

    def get_jwt_identity(self):
        return {
            'user_id': self.user_id,
            'role': self.role
        }
class Feedback(db.Model):
    __tablename__ = 'feedback'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    feedback_text = db.Column(db.Text)
    feedback_date = db.Column(db.DateTime, nullable=False)
    feedback_rating = db.Column(db.Integer, nullable=False)
