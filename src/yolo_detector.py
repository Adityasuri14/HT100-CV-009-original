#!/usr/bin/env python3
"""
YOLOv8 Detection Handler
Manages YOLOv8 model loading and vehicle detection.
"""

import os
import numpy as np
from ultralytics import YOLO
from pathlib import Path


class YOLODetector:
    """
    Handles YOLOv8 model loading and vehicle detection.
    """
    
    # COCO dataset vehicle class IDs
    VEHICLE_CLASSES = {
        2: 'car',
        3: 'motorcycle',
        5: 'bus',
        7: 'truck'
    }
    
    def __init__(self, model_path='yolov8n.pt', confidence_threshold=0.5, device='cpu'):
        """
        Initialize YOLOv8 detector.
        
        Args:
            model_path (str): Path to YOLOv8 model file or model name
            confidence_threshold (float): Minimum confidence for detections (0-1)
            device (str): Device to run inference on ('cpu', 'cuda', or '0', '1', etc.)
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.device = device
        self.model = None
        
        # Load the model
        self._load_model()
    
    def _load_model(self):
        """Load YOLOv8 model."""
        try:
            # Check if model file exists
            if os.path.exists(self.model_path):
                print(f"  → Loading model from: {self.model_path}")
            else:
                # Model will be downloaded automatically by ultralytics
                print(f"  → Model not found locally. Downloading: {self.model_path}")
                # Ensure the models directory exists
                model_dir = Path(self.model_path).parent
                model_dir.mkdir(parents=True, exist_ok=True)
            
            # Load YOLOv8 model
            self.model = YOLO(self.model_path)
            
            # Move model to specified device
            self.model.to(self.device)
            
            print(f"  → Model loaded successfully on device: {self.device}")
            print(f"  → Confidence threshold: {self.confidence_threshold}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load YOLOv8 model: {e}")
    
    def detect(self, frame):
        """
        Detect vehicles in a frame.
        
        Args:
            frame (numpy.ndarray): Input image frame (RGB format)
            
        Returns:
            list: List of detections, each containing:
                  - bbox: [x1, y1, x2, y2]
                  - confidence: float
                  - class_id: int
                  - class_name: str
        """
        if frame is None or self.model is None:
            return []
        
        try:
            # Run inference
            results = self.model(
                frame,
                conf=self.confidence_threshold,
                verbose=False  # Suppress output
            )
            
            # Parse results
            detections = []
            
            for result in results:
                boxes = result.boxes
                
                if boxes is None or len(boxes) == 0:
                    continue
                
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Get confidence
                    confidence = float(box.conf[0])
                    
                    # Get class ID
                    class_id = int(box.cls[0])
                    
                    # Filter for vehicle classes only
                    if class_id in self.VEHICLE_CLASSES:
                        detection = {
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': confidence,
                            'class_id': class_id,
                            'class_name': self.VEHICLE_CLASSES[class_id]
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Warning: Detection failed: {e}")
            return []
    
    def detect_with_tracking(self, frame, persist=True):
        """
        Detect and track vehicles in a frame using YOLOv8 built-in tracking.
        
        Args:
            frame (numpy.ndarray): Input image frame (RGB format)
            persist (bool): Whether to persist tracks across frames
            
        Returns:
            list: List of detections with tracking IDs, each containing:
                  - bbox: [x1, y1, x2, y2]
                  - confidence: float
                  - class_id: int
                  - class_name: str
                  - track_id: int (if tracking is enabled)
        """
        if frame is None or self.model is None:
            return []
        
        try:
            # Run inference with tracking
            results = self.model.track(
                frame,
                conf=self.confidence_threshold,
                persist=persist,
                verbose=False
            )
            
            # Parse results
            detections = []
            
            for result in results:
                boxes = result.boxes
                
                if boxes is None or len(boxes) == 0:
                    continue
                
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Get confidence
                    confidence = float(box.conf[0])
                    
                    # Get class ID
                    class_id = int(box.cls[0])
                    
                    # Get track ID if available
                    track_id = int(box.id[0]) if box.id is not None else None
                    
                    # Filter for vehicle classes only
                    if class_id in self.VEHICLE_CLASSES:
                        detection = {
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': confidence,
                            'class_id': class_id,
                            'class_name': self.VEHICLE_CLASSES[class_id],
                            'track_id': track_id
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Warning: Detection with tracking failed: {e}")
            return []
    
    def set_confidence_threshold(self, threshold):
        """
        Update confidence threshold.
        
        Args:
            threshold (float): New confidence threshold (0-1)
        """
        if 0 <= threshold <= 1:
            self.confidence_threshold = threshold
        else:
            raise ValueError("Confidence threshold must be between 0 and 1")
    
    def get_model_info(self):
        """
        Get information about the loaded model.
        
        Returns:
            dict: Model information including task, classes, etc.
        """
        if self.model is None:
            return {}
        
        return {
            'model_path': self.model_path,
            'device': self.device,
            'confidence_threshold': self.confidence_threshold,
            'task': self.model.task,
            'names': self.model.names
        }
