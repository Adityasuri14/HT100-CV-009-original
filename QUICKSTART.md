# Quick Start Guide

Get TrafficVision up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed (`python --version`)
- ✅ SUMO installed (`sumo --version`)
- ✅ SUMO_HOME environment variable set (`echo $SUMO_HOME`)

❌ Missing something? See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## Installation (2 minutes)

### Step 1: Clone and Navigate
```bash
git clone https://github.com/yourusername/TrafficVision-SUMO-YOLOv8.git
cd TrafficVision-SUMO-YOLOv8
```

### Step 2: Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## First Run (3 minutes)

### Just Run It!
```bash
python src/main.py
```

That's it! The YOLOv8 model will download automatically on first run (may take 1-2 minutes).

## What to Expect

### You Should See:
1. **Console Output**:
   ```
   ============================================================
   TrafficVision-SUMO-YOLOv8 - Traffic Monitoring System
   ============================================================
   
   [1/3] Initializing SUMO simulation...
   ✓ SUMO simulation started successfully
   
   [2/3] Loading YOLOv8 model...
   ✓ YOLOv8 model loaded successfully
   
   [3/3] Initializing Pygame visualizer...
   ✓ Pygame visualizer initialized successfully
   ```

2. **SUMO Window**: Traffic simulation with moving vehicles
3. **Pygame Window**: Visualization with detection boxes

### Controls
- **ESC**: Exit
- **SPACE**: Pause/Resume

## Troubleshooting

### Problem: "SUMO_HOME not set"
```bash
# Windows:
set SUMO_HOME=C:\Program Files (x86)\Eclipse\Sumo

# Linux:
export SUMO_HOME="/usr/share/sumo"

# macOS:
export SUMO_HOME="/usr/local/opt/sumo/share/sumo"
```

### Problem: "Port 8813 already in use"
Another SUMO instance is running. Close it or modify the port in `src/main.py`.

### Problem: Slow performance
1. Try a smaller model:
   ```bash
   # Download smaller model
   python scripts/download_model.py --model yolov8n.pt
   ```
2. Or reduce confidence threshold in `src/yolo_detector.py`

## Next Steps

### Customize Your Setup
1. **Try Different Models**: 
   ```bash
   python scripts/download_model.py --model yolov8m.pt
   ```

2. **Modify Traffic Patterns**: 
   Edit `data/sumo_config/simple.rou.xml`

3. **Adjust Detection**: 
   Edit `src/yolo_detector.py` → change `confidence_threshold`

### Explore Features
- Check real-time FPS in the info panel
- Watch vehicle detection boxes (green=car, orange=motorcycle, blue=bus, red=truck)
- See detection count vs total vehicles

## Getting Help

- 📖 Full documentation: [README.md](README.md)
- 🔧 Detailed setup: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/yourusername/TrafficVision-SUMO-YOLOv8/issues)

## Success! 🎉

You're now running a complete traffic monitoring system with:
- ✅ Real-time traffic simulation (SUMO)
- ✅ AI-powered vehicle detection (YOLOv8)
- ✅ Interactive visualization (Pygame)

Enjoy exploring TrafficVision!
