from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship to CheckIn
    checkins = db.relationship('CheckIn', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class CheckIn(db.Model):
    __tablename__ = 'user_checkins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(20), nullable=False)  # Happy, Calm, Anxious, Sad
    body_feeling = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships to AI-generated content
    practice = db.relationship('Practice', backref='checkin', lazy=True, uselist=False)
    journal_prompt = db.relationship('JournalPrompt', backref='checkin', lazy=True, uselist=False)

    def __repr__(self):
        return f'<CheckIn {self.mood} by User {self.user_id} at {self.created_at}>'


class Practice(db.Model):
    """AI-generated mindfulness practice"""
    __tablename__ = 'practices'

    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    practice_type = db.Column(db.String(50), nullable=False)  # breathing, meditation, movement, grounding
    audio_file = db.Column(db.String(255), nullable=True)  # OpenAI TTS audio filename
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Practice {self.title} for CheckIn {self.checkin_id}>'


class JournalPrompt(db.Model):
    """AI-generated journal prompt"""
    __tablename__ = 'journal_prompts'

    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'), nullable=False)
    prompt_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<JournalPrompt for CheckIn {self.checkin_id}>'

'''--------| TEST SPRINT 0 | DATABASE CONFIGS | ---------
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))
----------------------------------------------------- '''