#!/usr/bin/env python3
"""
Pygame Visualization Handler
Manages Pygame window and visualization of SUMO simulation with YOLOv8 detections.
"""

import pygame
import numpy as np
from PIL import Image


class PygameVisualizer:
    """
    Handles Pygame window creation and visualization of detections.
    """
    
    # Color scheme
    COLORS = {
        'car': (0, 255, 0),        # Green
        'motorcycle': (255, 165, 0),  # Orange
        'bus': (0, 191, 255),      # Deep Sky Blue
        'truck': (255, 0, 0),      # Red
        'default': (255, 255, 0)   # Yellow
    }
    
    BG_COLOR = (30, 30, 30)        # Dark gray
    TEXT_COLOR = (255, 255, 255)   # White
    INFO_BG_COLOR = (0, 0, 0, 180) # Semi-transparent black
    
    def __init__(self, width=1280, height=720, title="TrafficVision"):
        """
        Initialize Pygame visualizer.
        
        Args:
            width (int): Window width
            height (int): Window height
            title (str): Window title
        """
        self.width = width
        self.height = height
        self.title = title
        
        # Initialize Pygame
        pygame.init()
        
        # Create window
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        
        print(f"  → Window size: {width}x{height}")
    
    def draw_frame(self, frame, detections, fps=0, vehicle_count=0):
        """
        Draw a frame with detections overlay.
        
        Args:
            frame (numpy.ndarray): Background frame (SUMO screenshot)
            detections (list): List of detection dictionaries
            fps (float): Current FPS
            vehicle_count (int): Total number of vehicles in simulation
        """
        # Convert numpy array to Pygame surface
        if frame is not None:
            frame_surface = self._numpy_to_surface(frame)
            # Scale frame to fit window
            frame_surface = pygame.transform.scale(frame_surface, (self.width, self.height))
            self.screen.blit(frame_surface, (0, 0))
        else:
            # Fill with background color if no frame
            self.screen.fill(self.BG_COLOR)
        
        # Draw detections
        if detections:
            self._draw_detections(detections, frame.shape if frame is not None else None)
        
        # Draw info panel
        self._draw_info_panel(fps, vehicle_count, len(detections))
        
        # Update display
        pygame.display.flip()
    
    def _numpy_to_surface(self, array):
        """
        Convert numpy array to Pygame surface.
        
        Args:
            array (numpy.ndarray): Image array (RGB format)
            
        Returns:
            pygame.Surface: Pygame surface
        """
        # Ensure array is in the correct format
        if array.dtype != np.uint8:
            array = array.astype(np.uint8)
        
        # Create surface from array
        # Pygame uses (width, height) while numpy uses (height, width)
        surface = pygame.surfarray.make_surface(np.transpose(array, (1, 0, 2)))
        
        return surface
    
    def _draw_detections(self, detections, frame_shape):
        """
        Draw bounding boxes and labels for detections.
        
        Args:
            detections (list): List of detection dictionaries
            frame_shape (tuple): Shape of original frame (height, width, channels)
        """
        # Calculate scaling factors if frame was resized
        if frame_shape is not None:
            scale_x = self.width / frame_shape[1]
            scale_y = self.height / frame_shape[0]
        else:
            scale_x = scale_y = 1.0
        
        for detection in detections:
            bbox = detection['bbox']
            class_name = detection['class_name']
            confidence = detection['confidence']
            track_id = detection.get('track_id', None)
            
            # Scale bounding box coordinates
            x1 = int(bbox[0] * scale_x)
            y1 = int(bbox[1] * scale_y)
            x2 = int(bbox[2] * scale_x)
            y2 = int(bbox[3] * scale_y)
            
            # Get color for this class
            color = self.COLORS.get(class_name, self.COLORS['default'])
            
            # Draw bounding box
            pygame.draw.rect(
                self.screen,
                color,
                (x1, y1, x2 - x1, y2 - y1),
                2  # Line thickness
            )
            
            # Prepare label text
            if track_id is not None:
                label = f"{class_name} #{track_id} ({confidence:.2f})"
            else:
                label = f"{class_name} ({confidence:.2f})"
            
            # Draw label background
            label_surface = self.font_small.render(label, True, self.TEXT_COLOR)
            label_rect = label_surface.get_rect()
            
            # Position label above bounding box
            label_x = x1
            label_y = max(0, y1 - label_rect.height - 2)
            
            # Draw semi-transparent background for label
            background_rect = pygame.Rect(
                label_x,
                label_y,
                label_rect.width + 4,
                label_rect.height + 2
            )
            background_surface = pygame.Surface(
                (background_rect.width, background_rect.height),
                pygame.SRCALPHA
            )
            background_surface.fill((*color, 180))
            self.screen.blit(background_surface, (label_x, label_y))
            
            # Draw label text
            self.screen.blit(label_surface, (label_x + 2, label_y + 1))
    
    def _draw_info_panel(self, fps, vehicle_count, detection_count):
        """
        Draw information panel with stats.
        
        Args:
            fps (float): Current FPS
            vehicle_count (int): Total vehicles in simulation
            detection_count (int): Number of detected vehicles
        """
        # Panel dimensions
        panel_width = 280
        panel_height = 120
        panel_x = self.width - panel_width - 10
        panel_y = 10
        
        # Draw semi-transparent background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.INFO_BG_COLOR)
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # Draw title
        title_surface = self.font_medium.render("System Status", True, self.TEXT_COLOR)
        self.screen.blit(title_surface, (panel_x + 10, panel_y + 10))
        
        # Draw FPS
        fps_text = f"FPS: {fps:.1f}"
        fps_surface = self.font_small.render(fps_text, True, self.TEXT_COLOR)
        self.screen.blit(fps_surface, (panel_x + 10, panel_y + 40))
        
        # Draw vehicle count
        vehicle_text = f"Total Vehicles: {vehicle_count}"
        vehicle_surface = self.font_small.render(vehicle_text, True, self.TEXT_COLOR)
        self.screen.blit(vehicle_surface, (panel_x + 10, panel_y + 65))
        
        # Draw detection count
        detection_text = f"Detected: {detection_count}"
        detection_surface = self.font_small.render(detection_text, True, self.TEXT_COLOR)
        self.screen.blit(detection_surface, (panel_x + 10, panel_y + 90))
        
        # Draw legend for vehicle types
        legend_y = panel_y + panel_height + 20
        legend_surface = self.font_small.render("Vehicle Types:", True, self.TEXT_COLOR)
        self.screen.blit(legend_surface, (panel_x + 10, legend_y))
        
        y_offset = legend_y + 25
        for vehicle_type, color in self.COLORS.items():
            if vehicle_type != 'default':
                # Draw color box
                pygame.draw.rect(
                    self.screen,
                    color,
                    (panel_x + 10, y_offset, 15, 15)
                )
                
                # Draw label
                label_surface = self.font_small.render(
                    vehicle_type.capitalize(),
                    True,
                    self.TEXT_COLOR
                )
                self.screen.blit(label_surface, (panel_x + 30, y_offset))
                
                y_offset += 20
    
    def draw_text(self, text, position, font_size='medium', color=None):
        """
        Draw text at a specific position.
        
        Args:
            text (str): Text to draw
            position (tuple): (x, y) position
            font_size (str): 'small', 'medium', or 'large'
            color (tuple): RGB color tuple
        """
        if color is None:
            color = self.TEXT_COLOR
        
        # Select font
        if font_size == 'small':
            font = self.font_small
        elif font_size == 'large':
            font = self.font_large
        else:
            font = self.font_medium
        
        # Render and draw text
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)
    
    def clear(self):
        """Clear the screen."""
        self.screen.fill(self.BG_COLOR)
    
    def close(self):
        """Close Pygame and clean up resources."""
        pygame.quit()
