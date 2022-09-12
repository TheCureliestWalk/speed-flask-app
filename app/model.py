from app import db

class SpeedData(db.Model):
    __bind_key__ = 'local'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    location = db.Column(db.Integer())
    speed = db.Column(db.Integer())