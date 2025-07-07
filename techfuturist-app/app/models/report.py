# app/models/report.py

from app import db
from datetime import datetime
import enum

class ReportStatusEnum(enum.Enum):
    Submitted = "Soumis"
    InReview = "En Revue"
    Approved = "Approuvé"
    Rejected = "Rejeté"

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    feedback = db.Column(db.Text)
    
    submission_deadline = db.Column(db.DateTime)
    
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reports', lazy=True))
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    status = db.Column(
        db.Enum(ReportStatusEnum, name="report_status_enum"),
        default=ReportStatusEnum.Submitted,
        nullable=False
    )
  