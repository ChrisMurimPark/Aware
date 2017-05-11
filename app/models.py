import bcrypt
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, first_name, last_name, email, password, confirmed):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),
                bcrypt.gensalt())
        self.confirmed = confirmed
            
    # returns true unless a user should not be allowed to authenticate
    @property
    def is_authenticated(self):
        return True

    # returns true unless a user is inactive, like if they were banned
    @property
    def is_active(self):
        return True

    # returns true only for fake users who are not supposed to log into the system
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python 2
        except NameError:
            return str(self.id) # python 3

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password.encode('utf-8'), self.password)
        return self.password == pwhash


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)
    cost = db.Column(db.Float, index=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='category', lazy='dynamic')

