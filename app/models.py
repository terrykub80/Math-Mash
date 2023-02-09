from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import random, time


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    high_score = db.Column(db.Integer, nullable=False, default=0)
    scores = db.relationship('Score', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)


    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'email', 'username'}:
                setattr(self, key, value)
        db.session.commit()


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    points = db.Column(db.Integer, nullable=False, default=0)
    operator = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # SQL Equivalent - FOREIGN KEY(user_id) REFERENCES user(id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Score {self.points} | {self.date_created}>"



##########
# class Equations():
    
#     def generate_equation():
#         operators = ['+', '-', '*', '/']
#         operator = random.choice(operators)
#         num1 = random.randint(1, 10)
#         num2 = random.randint(1, 10)
#         equation = str(num1) + operator + str(num2)
#         correct_answer = eval(equation)
#         wrong_answers = [correct_answer + random.randint(1, 10),
#                         correct_answer + random.randint(1, 10),
#                         correct_answer + random.randint(1, 10)]
#         return equation, correct_answer, wrong_answers

    
#     equation, correct_answer, wrong_answers = generate_equation()
#     score = 0
#     print("Equation:", equation)
#     print("Correct Answer:", correct_answer)
#     print("Wrong Answers:", wrong_answers)

#     def handle_answers(self, answer_guess):
#         if answer_guess == self.correct_answer:
#             score += 1
#             generate_equation()
#         else:
#             generate_equation()
