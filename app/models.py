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

    # Relationships
    checkins = db.relationship('CheckIn', backref='user', lazy=True)
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True)
    practice_feedbacks = db.relationship('PracticeFeedback', backref='user', lazy=True)

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
    time_of_day = db.Column(db.String(10), nullable=False)  # Morning or Night
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships to AI-generated content and user responses
    practice = db.relationship('Practice', backref='checkin', lazy=True, uselist=False)
    journal_entry = db.relationship('JournalEntry', backref='checkin', lazy=True, uselist=False)

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
    journal_prompt = db.Column(db.Text, nullable=False)  # AI-generated journal prompt
    audio_file = db.Column(db.String(255), nullable=True)  # ElevenLabs TTS audio filename
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship to feedback
    feedback = db.relationship('PracticeFeedback', backref='practice', lazy=True, uselist=False)

    def __repr__(self):
        return f'<Practice {self.title} for CheckIn {self.checkin_id}>'


class JournalEntry(db.Model):
    """User's journal reflection entry"""
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_text = db.Column(db.Text, nullable=False)  # Response to AI-generated prompt

    # Time-specific structured responses
    intention_for_day = db.Column(db.String(500), nullable=True)  # Morning only
    self_care_today = db.Column(db.String(500), nullable=True)  # Night only
    goal_for_tomorrow = db.Column(db.String(500), nullable=True)  # Night only

    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<JournalEntry for CheckIn {self.checkin_id}>'


class PracticeFeedback(db.Model):
    """User feedback on mindfulness practice"""
    __tablename__ = 'practice_feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practices.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 (emoji scale: 😞 😐 🙂 😊 🤩)
    helped = db.Column(db.Boolean, nullable=True)  # Did this help?
    pacing = db.Column(db.String(20), nullable=True)  # Too fast, Just right, Too slow
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<PracticeFeedback rating={self.rating} for Practice {self.practice_id}>'


'''--------| TEST SPRINT 0 | DATABASE CONFIGS | ---------
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))
----------------------------------------------------- '''