# app/models/question.py

from app import db
import enum
from datetime import datetime

class QuestionTypeEnum(enum.Enum):
    QCM = "QCM"
    Open = "Ouvert"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(QuestionTypeEnum), nullable=False)
    
    options = db.Column(db.JSON)  # Utilisé uniquement pour les QCM
    correct_answer = db.Column(db.String(255))

    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    test = db.relationship('Test', backref=db.backref('questions', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)