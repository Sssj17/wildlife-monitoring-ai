# 🦁 AI-Based Wildlife Monitoring System

An advanced full-stack web application that uses artificial intelligence to detect and classify wildlife species from images, map sightings geographically, and provide real-time analytics for conservation efforts.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-AI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔍 AI-Powered Detection
- **YOLOv8 Integration**: State-of-the-art object detection model
- **Multi-Species Recognition**: Detects 10+ wildlife species including elephants, giraffes, zebras, bears, and more
- **Confidence Scoring**: Each detection includes confidence percentage
- **Visual Annotations**: Automatic bounding box drawing on detected animals

### 🗺️ GIS Mapping
- **Interactive Map**: Leaflet.js-powered map showing all sightings
- **Location Tracking**: GPS coordinates for each sighting
- **Geolocation Support**: One-click location capture from browser
- **Marker Clustering**: Organized visualization of multiple sightings

### 📊 Real-Time Analytics
- **Species Statistics**: Count and confidence metrics per species
- **Visual Dashboard**: Beautiful charts and graphs
- **Latest Sightings**: Comprehensive table with filtering
- **Data Export**: Easy access to all sighting records

### 🎨 Premium UI/UX
- **Dark Mode Design**: Eye-friendly interface with nature-inspired colors
- **Glassmorphism**: Modern frosted glass aesthetic
- **Smooth Animations**: Micro-interactions for enhanced experience
- **Fully Responsive**: Works seamlessly on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd C:\Users\SHIVANI\.gemini\antigravity\scratch\wildlife-monitoring-ai
```

2. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Start the Flask server**:
```bash
python app.py
```

The server will start on `http://localhost:5000`

4. **Access the application**:
Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Reporting a Wildlife Sighting

1. **Upload Image**: 
   - Click "Choose Image" or drag & drop a wildlife photo
   - Supported formats: JPG, PNG, GIF (max 16MB)

2. **Add Location (Optional)**:
   - Click "Use My Location" to auto-fill GPS coordinates
   - Or manually enter latitude/longitude
   - Add a descriptive location name

3. **Detect Wildlife**:
   - Click "Detect Wildlife" button
   - AI will analyze the image and identify species
   - Results show species name and confidence score

4. **View Results**:
   - See annotated image with bounding boxes
   - Sighting automatically appears on the map
   - Statistics update in real-time

### Managing Sightings

- **View All Sightings**: Scroll to the "Recent Sightings" table
- **Click Map Markers**: See sighting details in popup
- **Delete Sightings**: Use the delete button in the table
- **Refresh Data**: Click the refresh button to update

## 🛠️ Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **SQLAlchemy**: ORM for database management
- **SQLite**: Embedded SQL database
- **Ultralytics YOLOv8**: AI detection model
- **OpenCV**: Image processing
- **Pillow**: Image manipulation

### Frontend
- **Vanilla JavaScript**: No framework overhead
- **Leaflet.js**: Interactive mapping library
- **CSS3**: Modern styling with animations
- **HTML5**: Semantic markup

### AI/ML
- **YOLOv8 Nano**: Fast, lightweight object detection
- **Pretrained on COCO dataset**: 80 object classes
- **Wildlife filtering**: Custom logic for relevant species

## 📁 Project Structure

```
wildlife-monitoring-ai/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── ml_detector.py      # AI detection pipeline
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main dashboard UI
│   ├── styles.css          # Styling and animations
│   └── app.js              # Frontend logic
├── uploads/                # Original uploaded images
├── static/                 # Annotated detection images
├── database/
│   └── wildlife.db         # SQLite database
└── README.md               # This file
```

## 🔌 API Endpoints

### `POST /api/upload`
Upload image for wildlife detection
- **Body**: multipart/form-data with `image` file
- **Optional**: `latitude`, `longitude`, `location_name`
- **Returns**: Detection results and sighting IDs

### `GET /api/sightings`
Retrieve all wildlife sightings
- **Returns**: Array of sighting objects

### `GET /api/sightings/<id>`
Get specific sighting by ID
- **Returns**: Single sighting object

### `DELETE /api/sightings/<id>`
Delete a sighting
- **Returns**: Success message

### `GET /api/species`
Get species statistics
- **Returns**: Array with counts and confidence per species

## 🌟 Supported Wildlife Species

The system currently recognizes these species from the COCO dataset:

- 🐦 **Bird** - Various bird species
- 🐘 **Elephant** - African and Asian elephants
- 🦒 **Giraffe** - Long-necked beauties
- 🦓 **Zebra** - Striped equines
- 🐻 **Bear** - Various bear species
- 🐴 **Horse** - Wild and domestic horses
- 🐄 **Cow** - Cattle species
- 🐑 **Sheep** - Wool-bearing animals
- 🐱 **Cat** - Felines (wild and domestic)
- 🐕 **Dog** - Canines (wild and domestic)

## 🚀 Future Enhancements

### Short-term
- [ ] Add user authentication and profiles
- [ ] Export data to CSV/Excel
- [ ] Advanced filtering and search
- [ ] Multiple image upload
- [ ] Mobile app version

### Long-term
- [ ] Fine-tune model on specialized wildlife datasets (Snapshot Serengeti, iNaturalist)
- [ ] Add more species recognition
- [ ] Video processing capabilities
- [ ] Predictive analytics for poaching hotspots
- [ ] Integration with conservation databases
- [ ] Real-time camera trap integration
- [ ] Behavioral analysis (feeding, mating, migration)

## 🎓 Use Cases

### Conservation Organizations
- Monitor endangered species populations
- Track migration patterns
- Identify poaching hotspots

### Research Institutions
- Collect citizen science data
- Study animal behavior
- Population density analysis

### Wildlife Parks & Reserves
- Visitor sighting reports
- Resource allocation planning
- Educational programs

## 🐛 Troubleshooting

### Model Not Loading
If you get an error about the YOLO model:
```bash
pip install --upgrade ultralytics
```

### CORS Errors
Make sure Flask-CORS is installed:
```bash
pip install Flask-CORS
```

### Database Issues
Delete and recreate the database:
```bash
rm database/wildlife.db
# Restart the Flask server
```

### Port Already in Use
Change the port in `backend/config.py`:
```python
PORT = 5001  # or any available port
```

## 📝 License

This project is licensed under the MIT License - feel free to use it for educational and commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💡 Acknowledgments

- **Ultralytics** for the amazing YOLOv8 model
- **Leaflet.js** for mapping capabilities
- **Flask** community for excellent documentation
- Conservation organizations worldwide for inspiration

## 📧 Contact

For questions, suggestions, or collaborations, feel free to reach out!

---

**Built with ❤️ for Wildlife Conservation**

*This project demonstrates the power of AI in conservation efforts and serves as a strong portfolio piece for computer science students interested in environmental technology.*
