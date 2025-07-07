# app/models/project.py

from app import db
from datetime import datetime
import enum

class ProjectStatusEnum(enum.Enum):
    Submitted = "Soumis"
    InReview = "En Revue"
    Approved = "Approuvé"
    Rejected = "Rejeté"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('projects', lazy=True))
    
    status = db.Column(db.Enum(ProjectStatusEnum), default=ProjectStatusEnum.Submitted, nullable=False)
    feedback = db.Column(db.Text)
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
