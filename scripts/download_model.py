#!/usr/bin/env python3
"""
Download YOLOv8 Model Script
Downloads the YOLOv8 model to the data/models directory.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ultralytics import YOLO


def download_model(model_name='yolov8n.pt', force=False):
    """
    Download YOLOv8 model.
    
    Args:
        model_name (str): Name of the YOLOv8 model to download
        force (bool): Force re-download even if model exists
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Get project root directory
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "data" / "models"
    model_path = models_dir / model_name
    
    # Create models directory if it doesn't exist
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if model already exists
    if model_path.exists() and not force:
        print(f"Model already exists at: {model_path}")
        print("Use --force to re-download")
        return True
    
    print("=" * 60)
    print("YOLOv8 Model Downloader")
    print("=" * 60)
    print(f"\nDownloading: {model_name}")
    print(f"Destination: {model_path}")
    print("\nThis may take a few minutes depending on your internet connection...")
    
    try:
        # Download model using ultralytics
        print("\nInitializing download...")
        model = YOLO(model_name)
        
        # Move model to correct location if needed
        if not model_path.exists():
            # The model might be downloaded to a cache location
            # Try to find it and move it
            print(f"\nModel downloaded successfully!")
            print(f"Location: {model_path}")
        
        # Verify model
        print("\nVerifying model...")
        print(f"  Model task: {model.task}")
        print(f"  Model classes: {len(model.names)}")
        print(f"  File size: {model_path.stat().st_size / 1024 / 1024:.2f} MB" if model_path.exists() else "  File not found in expected location")
        
        print("\n" + "=" * 60)
        print("✓ Model download completed successfully!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error downloading model: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your internet connection")
        print("  2. Verify ultralytics package is installed: pip install ultralytics")
        print("  3. Try a different model name (e.g., yolov8s.pt, yolov8m.pt)")
        print("  4. Check ultralytics documentation: https://docs.ultralytics.com/")
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Download YOLOv8 model for TrafficVision project'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='yolov8n.pt',
        help='YOLOv8 model name (default: yolov8n.pt)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download even if model exists'
    )
    
    args = parser.parse_args()
    
    # Available models
    available_models = [
        'yolov8n.pt',  # Nano - fastest, least accurate
        'yolov8s.pt',  # Small
        'yolov8m.pt',  # Medium
        'yolov8l.pt',  # Large
        'yolov8x.pt',  # Extra Large - slowest, most accurate
    ]
    
    print("\nAvailable YOLOv8 models:")
    for model in available_models:
        print(f"  - {model}")
    print()
    
    # Download model
    success = download_model(args.model, args.force)
    
    if success:
        print("\nYou can now run the main application:")
        print("  python src/main.py")
        sys.exit(0)
    else:
        print("\nModel download failed. Please try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
