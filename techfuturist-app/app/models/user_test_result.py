# app/models/user_test_result.py

from app import db
from datetime import datetime

class UserTestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('test_results', lazy=True))
    test = db.relationship('Test', backref=db.backref('results', lazy=True))

    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
