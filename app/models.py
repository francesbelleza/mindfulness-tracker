from app import db

class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))
