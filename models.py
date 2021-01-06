from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect database with the provided flask app"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable = False, unique = True, primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)

    @classmethod
    def register(cls, username, pwd, email, first, last):
        """register user with hashed password and return an user object"""
        hashed = bcrypt.generate_password_hash(pwd)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return an instance of user with hased password        
        return cls(username = username, password = hashed_utf8, email = email, first_name = first, last_name = last) 

    @classmethod
    def authenticate(cls, username, password):
        """validate user with password"""
        u = User.query.filter_by(username = username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else: 
            return False
    
class Feedback(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String, db.ForeignKey('users.username'))

    user = db.relationship('User', backref = 'feedbacks')

