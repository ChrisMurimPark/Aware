import bcrypt
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),
                bcrypt.gensalt())
            
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

    def __repr__(self):
        return '<User {} {} {} {} {}>'.format(self.id, self.first_name, self.last_name,
                self.email, self.password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    date = db.Column(db.Date, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Transaction {} category_id:{} user_id:{} {} {}>'.format(
                self.id, self.category_id, self.user_id, self.name, self.date)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('Transaction', backref='category', lazy='dynamic')

