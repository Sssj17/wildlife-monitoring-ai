from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Sighting(db.Model):
    """Wildlife sighting record with detection details and location"""
    __tablename__ = 'sightings'
    
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location_name = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    detected_image_path = db.Column(db.String(500), nullable=True)
    
    def to_dict(self):
        """Convert sighting to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'species': self.species,
            'confidence': round(self.confidence, 2),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'location_name': self.location_name,
            'timestamp': self.timestamp.isoformat(),
            'image_path': self.image_path,
            'detected_image_path': self.detected_image_path
        }
    
    def __repr__(self):
        return f'<Sighting {self.species} at {self.timestamp}>'
