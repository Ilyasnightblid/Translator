from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_photo = db.Column(db.String(200), default='default_avatar.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with translations
    translations = db.relationship('Translation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_translation_stats(self):
        """Get user translation statistics"""
        total = self.translations.count()
        voice_count = self.translations.filter_by(translation_type='voice').count()
        file_count = self.translations.filter_by(translation_type='file').count()
        
        voice_percentage = (voice_count / total * 100) if total > 0 else 0
        file_percentage = (file_count / total * 100) if total > 0 else 0
        
        # Get top 3 languages
        language_stats = db.session.query(
            Translation.target_language,
            db.func.count(Translation.id).label('count')
        ).filter_by(user_id=self.id).group_by(
            Translation.target_language
        ).order_by(db.desc('count')).limit(3).all()
        
        return {
            'total': total,
            'voice_count': voice_count,
            'file_count': file_count,
            'voice_percentage': round(voice_percentage, 1),
            'file_percentage': round(file_percentage, 1),
            'top_languages': language_stats
        }

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text, nullable=False)
    source_language = db.Column(db.String(10), nullable=False)
    target_language = db.Column(db.String(10), nullable=False)
    translation_type = db.Column(db.String(20), nullable=False)  # 'voice' or 'file'
    filename = db.Column(db.String(200))  # For file translations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Translation {self.id}: {self.source_language} -> {self.target_language}>'
