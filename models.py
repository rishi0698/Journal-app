from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = 'entries'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    journal_notes = db.Column(db.Text, nullable=True)
    habits = db.Column(db.Text, nullable=True)      # stored as JSON string
    tracker = db.Column(db.Text, nullable=True)     # stored as JSON string
    reflection_good = db.Column(db.Text, nullable=True)
    reflection_bad = db.Column(db.Text, nullable=True)
    reflection_improve = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.String(50), nullable=False)
    
    def __init__(self, date, journal_notes=None, habits=None, tracker=None,
                 reflection_good=None, reflection_bad=None, reflection_improve=None):
        self.date = date
        self.journal_notes = journal_notes
        self.habits = json.dumps(habits) if habits else None
        self.tracker = json.dumps(tracker) if tracker else None
        self.reflection_good = reflection_good
        self.reflection_bad = reflection_bad
        self.reflection_improve = reflection_improve
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_habits(self):
        return json.loads(self.habits) if self.habits else {}
    
    def get_tracker(self):
        return json.loads(self.tracker) if self.tracker else {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'journal_notes': self.journal_notes,
            'habits': self.get_habits(),
            'tracker': self.get_tracker(),
            'reflection_good': self.reflection_good,
            'reflection_bad': self.reflection_bad,
            'reflection_improve': self.reflection_improve,
            'created_at': self.created_at
        }
