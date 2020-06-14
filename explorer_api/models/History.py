from datetime import datetime
from . import db


class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)
    house_info = db.Column(db.JSON, nullable=False)
    house_coords = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, house_info, house_coords):
        self.user_id = user_id
        self.house_info = house_info
        self.house_coords = house_coords
        self.added_at = datetime.now().date()

    def __repr__(self):
        return "<History entry by user %r at %r>" % (self.user_id, self.added_at)
