// API Configuration
const API_URL = 'http://localhost:5000/api';

// Global state
let map;
let markers = [];
let sightings = [];

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const clearBtn = document.getElementById('clearBtn');
const previewArea = document.getElementById('previewArea');
const previewImage = document.getElementById('previewImage');
const uploadBtn = document.getElementById('uploadBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const detectionResults = document.getElementById('detectionResults');
const resultsContent = document.getElementById('resultsContent');
const getLocationBtn = document.getElementById('getLocationBtn');
const latitudeInput = document.getElementById('latitude');
const longitudeInput = document.getElementById('longitude');
const locationNameInput = document.getElementById('locationName');
const refreshBtn = document.getElementById('refreshBtn');
const sightingsBody = document.getElementById('sightingsBody');
const statsChart = document.getElementById('statsChart');
const statsEmpty = document.getElementById('statsEmpty');

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadSightings();
    loadStats();
    setupEventListeners();
});

// ===== Map Initialization =====
function initMap() {
    // Initialize Leaflet map centered on Africa (good for wildlife)
    map = L.map('map').setView([0, 20], 3);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
}

// ===== Event Listeners =====
function setupEventListeners() {
    // File input
    browseBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Clear preview
    clearBtn.addEventListener('click', clearPreview);

    // Upload button
    uploadBtn.addEventListener('click', uploadImage);

    // Get location
    getLocationBtn.addEventListener('click', getCurrentLocation);

    // Refresh sightings
    refreshBtn.addEventListener('click', () => {
        loadSightings();
        loadStats();
    });
}

// ===== File Handling =====
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        displayPreview(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        fileInput.files = e.dataTransfer.files;
        displayPreview(file);
    }
}

function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadArea.style.display = 'none';
        previewArea.style.display = 'block';
        uploadBtn.disabled = false;
        detectionResults.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function clearPreview() {
    fileInput.value = '';
    uploadArea.style.display = 'block';
    previewArea.style.display = 'none';
    uploadBtn.disabled = true;
    detectionResults.style.display = 'none';
}

// ===== Geolocation =====
function getCurrentLocation() {
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
        return;
    }

    getLocationBtn.textContent = '📍 Getting location...';
    getLocationBtn.disabled = true;

    navigator.geolocation.getCurrentPosition(
        (position) => {
            latitudeInput.value = position.coords.latitude.toFixed(6);
            longitudeInput.value = position.coords.longitude.toFixed(6);
            getLocationBtn.textContent = '✅ Location obtained';
            setTimeout(() => {
                getLocationBtn.textContent = '📍 Use My Location';
                getLocationBtn.disabled = false;
            }, 2000);
        },
        (error) => {
            alert('Unable to retrieve location: ' + error.message);
            getLocationBtn.textContent = '📍 Use My Location';
            getLocationBtn.disabled = false;
        }
    );
}

// ===== Image Upload & Detection =====
async function uploadImage() {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    // Add location data if available
    if (latitudeInput.value) {
        formData.append('latitude', latitudeInput.value);
    }
    if (longitudeInput.value) {
        formData.append('longitude', longitudeInput.value);
    }
    if (locationNameInput.value) {
        formData.append('location_name', locationNameInput.value);
    }

    // Show loading
    uploadBtn.disabled = true;
    loadingIndicator.style.display = 'block';
    detectionResults.style.display = 'none';

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
            loadSightings();
            loadStats();
        } else {
            alert('Detection failed: ' + data.error);
        }
    } catch (error) {
        alert('Upload failed: ' + error.message);
    } finally {
        loadingIndicator.style.display = 'none';
        uploadBtn.disabled = false;
    }
}

function displayResults(data) {
    detectionResults.style.display = 'block';

    if (data.detections.length === 0) {
        resultsContent.innerHTML = '<p>No wildlife detected in this image. Try another image!</p>';
        return;
    }

    let html = `<p class="upload-text">✅ ${data.message}</p>`;

    // Display detections
    data.detections.forEach(det => {
        html += `
            <div class="result-item">
                <span class="result-species">${det.species}</span>
                <span class="result-confidence">${(det.confidence * 100).toFixed(1)}%</span>
            </div>
        `;
    });

    // Display annotated image
    if (data.annotated_image) {
        html += `
            <div class="result-image">
                <img src="http://localhost:5000/static/${data.annotated_image}" alt="Detected wildlife">
            </div>
        `;
    }

    resultsContent.innerHTML = html;

    // Clear form
    setTimeout(() => {
        clearPreview();
        latitudeInput.value = '';
        longitudeInput.value = '';
        locationNameInput.value = '';
    }, 3000);
}

// ===== Load Sightings =====
async function loadSightings() {
    try {
        const response = await fetch(`${API_URL}/sightings`);
        sightings = await response.json();

        displaySightings(sightings);
        updateMap(sightings);
    } catch (error) {
        console.error('Failed to load sightings:', error);
    }
}

function displaySightings(data) {
    if (data.length === 0) {
        sightingsBody.innerHTML = '<tr><td colspan="6" class="empty-state">No sightings recorded yet</td></tr>';
        return;
    }

    sightingsBody.innerHTML = data.map(sighting => `
        <tr>
            <td><span class="species-badge">${sighting.species}</span></td>
            <td><span class="confidence-badge">${(sighting.confidence * 100).toFixed(1)}%</span></td>
            <td>${sighting.location_name || (sighting.latitude ? `${sighting.latitude.toFixed(4)}, ${sighting.longitude.toFixed(4)}` : 'Unknown')}</td>
            <td>${formatDate(sighting.timestamp)}</td>
            <td>
                ${sighting.detected_image_path ?
            `<img src="http://localhost:5000/static/${sighting.detected_image_path.split('\\').pop()}" 
                          alt="${sighting.species}" class="thumbnail">` :
            'N/A'}
            </td>
            <td>
                <button class="btn-delete" onclick="deleteSighting(${sighting.id})">🗑️ Delete</button>
            </td>
        </tr>
    `).join('');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ===== Map Updates =====
function updateMap(data) {
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Add new markers
    data.forEach(sighting => {
        if (sighting.latitude && sighting.longitude) {
            const marker = L.marker([sighting.latitude, sighting.longitude])
                .addTo(map)
                .bindPopup(`
                    <strong>${sighting.species}</strong><br>
                    Confidence: ${(sighting.confidence * 100).toFixed(1)}%<br>
                    ${sighting.location_name || ''}<br>
                    ${formatDate(sighting.timestamp)}
                `);
            markers.push(marker);
        }
    });

    // Fit bounds if markers exist
    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// ===== Statistics =====
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/species`);
        const stats = await response.json();

        displayStats(stats);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

function displayStats(stats) {
    if (stats.length === 0) {
        statsChart.style.display = 'none';
        statsEmpty.style.display = 'block';
        return;
    }

    statsChart.style.display = 'block';
    statsEmpty.style.display = 'none';

    // Find max count for scaling
    const maxCount = Math.max(...stats.map(s => s.count));

    statsChart.innerHTML = stats.map(stat => {
        const width = (stat.count / maxCount) * 100;
        return `
            <div class="stat-item">
                <div style="flex: 1;">
                    <div class="stat-species">
                        <span>${getSpeciesEmoji(stat.species)}</span>
                        <span>${stat.species}</span>
                    </div>
                    <div class="stat-bar" style="width: ${width}%"></div>
                </div>
                <span class="stat-count">${stat.count}</span>
            </div>
        `;
    }).join('');
}

function getSpeciesEmoji(species) {
    const emojis = {
        'bird': '🐦',
        'cat': '🐱',
        'dog': '🐕',
        'horse': '🐴',
        'sheep': '🐑',
        'cow': '🐄',
        'elephant': '🐘',
        'bear': '🐻',
        'zebra': '🦓',
        'giraffe': '🦒'
    };
    return emojis[species] || '🦁';
}

// ===== Delete Sighting =====
async function deleteSighting(id) {
    if (!confirm('Are you sure you want to delete this sighting?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/sightings/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadSightings();
            loadStats();
        } else {
            alert('Failed to delete sighting');
        }
    } catch (error) {
        alert('Delete failed: ' + error.message);
    }
}
