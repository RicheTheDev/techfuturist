# app/models/test.py

from app import db
from datetime import datetime
import enum

class TestTypeEnum(enum.Enum):
    QCM = "QCM"
    Open = "Ouvert"
    Practical = "Pratique"

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.Enum(TestTypeEnum), nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('created_tests', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
