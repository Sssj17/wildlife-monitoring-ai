import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import db, Sighting
from ml_detector import WildlifeDetector
import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)
app.secret_key = config.SECRET_KEY

# Initialize CORS with production-ready settings
if isinstance(config.CORS_ORIGINS, list):
    CORS(app, origins=config.CORS_ORIGINS)
else:
    CORS(app)

# Initialize database
db.init_app(app)

# Initialize ML detector
detector = WildlifeDetector()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# Create database tables
with app.app_context():
    db.create_all()
    print("Database initialized!")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Wildlife Monitoring API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """
    Upload image and detect wildlife
    
    Expected: multipart/form-data with 'image' file and optional 'latitude', 'longitude', 'location_name'
    Returns: Detection results and sighting ID
    """
    # Check if image file is present
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: ' + ', '.join(config.ALLOWED_EXTENSIONS)}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Get optional location data
    latitude = request.form.get('latitude', type=float)
    longitude = request.form.get('longitude', type=float)
    location_name = request.form.get('location_name', '')
    
    # Detect wildlife
    try:
        detections, annotated_path = detector.process_image(filepath, filename)
        
        if not detections:
            return jsonify({
                'message': 'No wildlife detected in image',
                'detections': []
            }), 200
        
        # Save each detection as a sighting
        sighting_ids = []
        for detection in detections:
            sighting = Sighting(
                species=detection['species'],
                confidence=detection['confidence'],
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                image_path=filepath,
                detected_image_path=annotated_path
            )
            db.session.add(sighting)
            db.session.flush()
            sighting_ids.append(sighting.id)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Detected {len(detections)} wildlife species!',
            'detections': detections,
            'sighting_ids': sighting_ids,
            'annotated_image': os.path.basename(annotated_path) if annotated_path else None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Detection failed: {str(e)}'}), 500

@app.route('/api/sightings', methods=['GET'])
def get_sightings():
    """Get all wildlife sightings"""
    try:
        sightings = Sighting.query.order_by(Sighting.timestamp.desc()).all()
        return jsonify([s.to_dict() for s in sightings]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sightings/<int:sighting_id>', methods=['GET'])
def get_sighting(sighting_id):
    """Get specific sighting by ID"""
    try:
        sighting = Sighting.query.get_or_404(sighting_id)
        return jsonify(sighting.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/sightings/<int:sighting_id>', methods=['DELETE'])
def delete_sighting(sighting_id):
    """Delete a sighting"""
    try:
        sighting = Sighting.query.get_or_404(sighting_id)
        db.session.delete(sighting)
        db.session.commit()
        return jsonify({'message': 'Sighting deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/species', methods=['GET'])
def get_species_stats():
    """Get species statistics"""
    try:
        # Count sightings per species
        from sqlalchemy import func
        stats = db.session.query(
            Sighting.species,
            func.count(Sighting.id).label('count'),
            func.avg(Sighting.confidence).label('avg_confidence')
        ).group_by(Sighting.species).all()
        
        result = [
            {
                'species': species,
                'count': count,
                'avg_confidence': round(avg_conf, 2)
            }
            for species, count, avg_conf in stats
        ]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded images"""
    return send_from_directory(config.UPLOAD_FOLDER, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (annotated images)"""
    return send_from_directory(config.STATIC_FOLDER, filename)

@app.route('/')
def index():
    """Serve frontend"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'index.html')

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
