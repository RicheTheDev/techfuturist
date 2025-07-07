# app/models/resource.py

# from app import db
# from datetime import datetime

# class Resource(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text)
#     file_url = db.Column(db.String(255), nullable=False)
#     file_type = db.Column(db.String(50), nullable=False)
    
#     uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('resources', lazy=True))
    
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from app import db
from datetime import datetime

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('resources', lazy=True))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ Ajouts pour le dashboard
    is_published = db.Column(db.Boolean, default=False)
    download_count = db.Column(db.Integer, default=0)
