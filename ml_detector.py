import os
import cv2
from ultralytics import YOLO
from config import MODEL_NAME, CONFIDENCE_THRESHOLD, WILDLIFE_CLASSES, STATIC_FOLDER

class WildlifeDetector:
    """AI-powered wildlife detection using YOLOv8"""
    
    def __init__(self):
        """Initialize YOLO model"""
        print("Loading YOLOv8 model...")
        self.model = YOLO(MODEL_NAME)
        print("Model loaded successfully!")
        
    def detect_wildlife(self, image_path):
        """
        Detect wildlife in image and return results
        
        Args:
            image_path (str): Path to uploaded image
            
        Returns:
            list: Detected animals with species, confidence, and bounding boxes
        """
        # Run inference
        results = self.model(image_path, conf=CONFIDENCE_THRESHOLD)
        
        detections = []
        
        # Process results
        for result in results:
            boxes = result.boxes
            names = result.names
            
            for box in boxes:
                # Get class name
                class_id = int(box.cls[0])
                class_name = names[class_id]
                
                # Only keep wildlife classes
                if class_name in WILDLIFE_CLASSES:
                    confidence = float(box.conf[0])
                    
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    detections.append({
                        'species': class_name,
                        'confidence': confidence,
                        'bbox': [x1, y1, x2, y2]
                    })
        
        return detections
    
    def draw_detections(self, image_path, detections, output_path):
        """
        Draw bounding boxes on image
        
        Args:
            image_path (str): Original image path
            detections (list): Detection results
            output_path (str): Path to save annotated image
            
        Returns:
            str: Path to saved image
        """
        # Read image
        img = cv2.imread(image_path)
        
        # Draw each detection
        for det in detections:
            x1, y1, x2, y2 = [int(coord) for coord in det['bbox']]
            species = det['species']
            confidence = det['confidence']
            
            # Draw rectangle
            color = (0, 255, 0)  # Green
            thickness = 3
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
            
            # Add label with species and confidence
            label = f"{species.capitalize()}: {confidence:.2f}"
            font_scale = 0.8
            font_thickness = 2
            
            # Get label size for background
            (label_width, label_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
            )
            
            # Draw background for text
            cv2.rectangle(
                img, 
                (x1, y1 - label_height - 10), 
                (x1 + label_width, y1), 
                color, 
                -1
            )
            
            # Draw text
            cv2.putText(
                img, 
                label, 
                (x1, y1 - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, 
                (0, 0, 0),  # Black text
                font_thickness
            )
        
        # Save annotated image
        cv2.imwrite(output_path, img)
        return output_path
    
    def process_image(self, image_path, filename):
        """
        Complete detection pipeline
        
        Args:
            image_path (str): Path to uploaded image
            filename (str): Original filename
            
        Returns:
            tuple: (detections, annotated_image_path)
        """
        # Detect wildlife
        detections = self.detect_wildlife(image_path)
        
        # Draw bounding boxes if detections found
        annotated_path = None
        if detections:
            output_filename = f"detected_{filename}"
            output_path = os.path.join(STATIC_FOLDER, output_filename)
            annotated_path = self.draw_detections(image_path, detections, output_path)
        
        return detections, annotated_path
