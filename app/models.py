from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    patronymic = db.Column(db.String)
    phone_number = db.Column(db.String, index=True, unique=True)
    patients = db.relationship('Patient', backref='medic', lazy='dynamic')

    def __repr__(self):
        return '{} {} {}'.format(self.second_name, self.first_name, self.patronymic)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    patronymic = db.Column(db.String)
    phone_number = db.Column(db.String, index=True, unique=True)
    age = db.Column(db.Integer)
    time_arrived = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    def __repr__(self):
        return '<Fist name={} second name={}>'.format(self.first_name, self.second_name)