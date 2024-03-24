from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    quiz_results = db.relationship('QuizResult', backref='user', lazy='dynamic')

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<QuizResult {}>'.format(self.score)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'correct_answer': self.correct_answer
            # Add more fields if needed
        }

    def __repr__(self):
        return '<QuizQuestion {}>'.format(self.question_text)
