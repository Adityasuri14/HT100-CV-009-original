#!/usr/bin/env python3
"""
Main entry point for TrafficVision-SUMO-YOLOv8 application.
Coordinates SUMO simulation, YOLOv8 detection, and Pygame visualization.
"""

import os
import sys
import time
import pygame
from pathlib import Path

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent))

from sumo_simulation import SumoSimulation
from yolo_detector import YOLODetector
from pygame_visualizer import PygameVisualizer


class TrafficVisionApp:
    """Main application class that coordinates all components."""
    
    def __init__(self):
        """Initialize the application and all components."""
        print("=" * 60)
        print("TrafficVision-SUMO-YOLOv8 - Traffic Monitoring System")
        print("=" * 60)
        
        # Get project root directory
        self.project_root = Path(__file__).parent.parent
        
        # Initialize components
        self.sumo_sim = None
        self.detector = None
        self.visualizer = None
        self.running = False
        self.paused = False
        
        # Performance metrics
        self.frame_count = 0
        self.start_time = None
        self.fps = 0
        
    def initialize_components(self):
        """Initialize SUMO simulation, YOLOv8 detector, and Pygame visualizer."""
        try:
            # Initialize SUMO simulation
            print("\n[1/3] Initializing SUMO simulation...")
            sumo_config_path = self.project_root / "data" / "sumo_config" / "simple.sumo.cfg"
            self.sumo_sim = SumoSimulation(str(sumo_config_path))
            print("✓ SUMO simulation started successfully")
            
            # Initialize YOLOv8 detector
            print("\n[2/3] Loading YOLOv8 model...")
            model_path = self.project_root / "data" / "models" / "yolov8n.pt"
            self.detector = YOLODetector(str(model_path))
            print("✓ YOLOv8 model loaded successfully")
            
            # Initialize Pygame visualizer
            print("\n[3/3] Initializing Pygame visualizer...")
            self.visualizer = PygameVisualizer(
                width=1280,
                height=720,
                title="TrafficVision - SUMO + YOLOv8"
            )
            print("✓ Pygame visualizer initialized successfully")
            
            print("\n" + "=" * 60)
            print("All components initialized successfully!")
            print("=" * 60)
            print("\nControls:")
            print("  ESC   - Exit application")
            print("  SPACE - Pause/Resume simulation")
            print("\nStarting main loop...\n")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Error during initialization: {e}")
            return False
    
    def process_frame(self):
        """Process a single frame: get SUMO screenshot, detect vehicles, visualize."""
        try:
            # Step the SUMO simulation
            self.sumo_sim.step()
            
            # Get current frame from SUMO
            frame = self.sumo_sim.get_screenshot()
            if frame is None:
                return False
            
            # Detect vehicles using YOLOv8
            detections = self.detector.detect(frame)
            
            # Get vehicle information from SUMO
            vehicle_ids = self.sumo_sim.get_vehicle_ids()
            
            # Visualize the frame with detections
            self.visualizer.draw_frame(
                frame=frame,
                detections=detections,
                fps=self.fps,
                vehicle_count=len(vehicle_ids)
            )
            
            return True
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return False
    
    def calculate_fps(self):
        """Calculate and update FPS."""
        self.frame_count += 1
        
        if self.frame_count % 10 == 0:  # Update FPS every 10 frames
            current_time = time.time()
            elapsed = current_time - self.start_time
            self.fps = self.frame_count / elapsed if elapsed > 0 else 0
    
    def handle_events(self):
        """Handle Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    status = "PAUSED" if self.paused else "RESUMED"
                    print(f"\nSimulation {status}")
    
    def run(self):
        """Main application loop."""
        # Initialize all components
        if not self.initialize_components():
            print("Failed to initialize components. Exiting...")
            return
        
        # Start timing
        self.running = True
        self.start_time = time.time()
        
        try:
            # Main loop
            while self.running:
                # Handle user input
                self.handle_events()
                
                # Process frame if not paused
                if not self.paused:
                    if not self.process_frame():
                        print("No more frames to process. Exiting...")
                        break
                    
                    # Calculate FPS
                    self.calculate_fps()
                
                # Small delay to control frame rate
                pygame.time.delay(10)
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Shutting down...")
        except Exception as e:
            print(f"\n\nUnexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources before exit."""
        print("\nCleaning up...")
        
        if self.sumo_sim:
            self.sumo_sim.close()
            print("✓ SUMO simulation closed")
        
        if self.visualizer:
            self.visualizer.close()
            print("✓ Pygame visualizer closed")
        
        # Print final statistics
        if self.frame_count > 0:
            elapsed = time.time() - self.start_time
            avg_fps = self.frame_count / elapsed if elapsed > 0 else 0
            print(f"\nSession Statistics:")
            print(f"  Total frames: {self.frame_count}")
            print(f"  Duration: {elapsed:.2f}s")
            print(f"  Average FPS: {avg_fps:.2f}")
        
        print("\nThank you for using TrafficVision!")


def main():
    """Entry point of the application."""
    # Create and run the application
    app = TrafficVisionApp()
    app.run()


if __name__ == "__main__":
    main()
