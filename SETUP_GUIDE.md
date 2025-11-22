# Setup Guide - TrafficVision-SUMO-YOLOv8

Complete step-by-step guide to set up and run the TrafficVision project.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installing SUMO](#installing-sumo)
3. [Python Environment Setup](#python-environment-setup)
4. [Project Configuration](#project-configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Ubuntu 20.04+, or macOS 10.15+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **GPU**: Optional (CUDA-capable GPU for faster inference)

### Recommended Requirements
- **RAM**: 16GB
- **GPU**: NVIDIA GPU with CUDA support
- **Storage**: 5GB free space

---

## Installing SUMO

### Windows

1. **Download SUMO**:
   - Visit [SUMO Downloads](https://sumo.dlr.de/docs/Downloads.php)
   - Download the latest Windows installer (e.g., `sumo-win64-1.15.0.msi`)

2. **Install SUMO**:
   - Run the installer
   - Default installation path: `C:\Program Files (x86)\Eclipse\Sumo`

3. **Set SUMO_HOME**:
   - Open System Properties → Environment Variables
   - Add new system variable:
     - Name: `SUMO_HOME`
     - Value: `C:\Program Files (x86)\Eclipse\Sumo`
   - Add to PATH: `%SUMO_HOME%\bin`

4. **Verify Installation**:
   ```cmd
   sumo --version
   ```

### Linux (Ubuntu/Debian)

1. **Add SUMO Repository**:
   ```bash
   sudo add-apt-repository ppa:sumo/stable
   sudo apt-get update
   ```

2. **Install SUMO**:
   ```bash
   sudo apt-get install sumo sumo-tools sumo-doc
   ```

3. **Set SUMO_HOME**:
   ```bash
   echo 'export SUMO_HOME="/usr/share/sumo"' >> ~/.bashrc
   echo 'export PATH="$PATH:$SUMO_HOME/bin"' >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Verify Installation**:
   ```bash
   sumo --version
   ```

### macOS

1. **Install via Homebrew**:
   ```bash
   brew tap dlr-ts/sumo
   brew install sumo
   ```

2. **Set SUMO_HOME**:
   ```bash
   echo 'export SUMO_HOME="/usr/local/opt/sumo/share/sumo"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify Installation**:
   ```bash
   sumo --version
   ```

---

## Python Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/TrafficVision-SUMO-YOLOv8.git
cd TrafficVision-SUMO-YOLOv8
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -c "import ultralytics; import pygame; import traci; print('All packages installed successfully!')"
```

---

## Project Configuration

### 1. Directory Structure
Ensure the following directories exist:
```bash
mkdir -p data/models
mkdir -p data/recordings
```

### 2. Download YOLOv8 Model
```bash
# Option 1: Use the download script
python scripts/download_model.py

# Option 2: Let it auto-download on first run
# The model will be downloaded automatically when you run main.py
```

### 3. GPU Support (Optional)
If you have an NVIDIA GPU and want to use it:

```bash
# Check if CUDA is available
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"

# If CUDA is available, modify src/yolo_detector.py:
# Change: device='cpu'
# To: device='cuda' or device='0'
```

---

## Running the Application

### Basic Usage
```bash
python src/main.py
```

### Command Line Controls
Once the application is running:
- **ESC**: Exit application
- **SPACE**: Pause/Resume simulation

### Expected Output
```
============================================================
TrafficVision-SUMO-YOLOv8 - Traffic Monitoring System
============================================================

[1/3] Initializing SUMO simulation...
  → TraCI connected on port 8813
  → Initial vehicles: 0
✓ SUMO simulation started successfully

[2/3] Loading YOLOv8 model...
  → Loading model from: data/models/yolov8n.pt
  → Model loaded successfully on device: cpu
  → Confidence threshold: 0.5
✓ YOLOv8 model loaded successfully

[3/3] Initializing Pygame visualizer...
  → Window size: 1280x720
✓ Pygame visualizer initialized successfully

============================================================
All components initialized successfully!
============================================================

Controls:
  ESC   - Exit application
  SPACE - Pause/Resume simulation

Starting main loop...
```

---

## Troubleshooting

### Issue: SUMO_HOME not set
**Error**: `EnvironmentError: SUMO_HOME environment variable not set`

**Solution**:
1. Verify SUMO is installed: `sumo --version`
2. Check SUMO_HOME: `echo $SUMO_HOME` (Linux/macOS) or `echo %SUMO_HOME%` (Windows)
3. Set SUMO_HOME as described in [Installing SUMO](#installing-sumo)
4. Restart terminal/command prompt

### Issue: TraCI Connection Failed
**Error**: `ConnectionError: Failed to start SUMO simulation`

**Solution**:
1. Check if port 8813 is available:
   ```bash
   # Linux/macOS
   netstat -an | grep 8813
   
   # Windows
   netstat -an | findstr 8813
   ```
2. Close any other SUMO instances
3. Try a different port in `src/main.py`:
   ```python
   self.sumo_sim = SumoSimulation(str(sumo_config_path), port=8814)
   ```

### Issue: Model Download Failed
**Error**: `RuntimeError: Failed to load YOLOv8 model`

**Solution**:
1. Check internet connection
2. Manually download model:
   ```bash
   python scripts/download_model.py --model yolov8n.pt --force
   ```
3. Try a different model size:
   ```bash
   python scripts/download_model.py --model yolov8s.pt
   ```

### Issue: Low FPS
**Problem**: Application runs slowly (<10 FPS)

**Solutions**:
1. Use smaller YOLOv8 model (yolov8n.pt instead of yolov8x.pt)
2. Reduce SUMO GUI quality:
   - In SUMO GUI: Edit → Edit Visualization → Vehicle Quality → Low
3. Use GPU if available:
   - Modify `src/yolo_detector.py`: `device='cuda'`
4. Reduce simulation step length in `simple.sumo.cfg`

### Issue: No Detections
**Problem**: YOLOv8 not detecting any vehicles

**Solutions**:
1. Lower confidence threshold in `src/yolo_detector.py`:
   ```python
   self.confidence_threshold = 0.3  # Instead of 0.5
   ```
2. Verify SUMO vehicles are visible in GUI
3. Check screenshot capture is working (temp_screenshot.png should be created)

### Issue: Pygame Window Not Responding
**Problem**: Pygame window freezes or doesn't update

**Solutions**:
1. Ensure pygame is properly installed: `pip install --upgrade pygame`
2. Check system graphics drivers are up to date
3. Try running without SUMO GUI:
   - Modify `src/main.py`: `self.sumo_sim = SumoSimulation(..., gui=False)`

---

## Performance Optimization

### For Better FPS
1. **Use GPU**: Set `device='cuda'` in yolo_detector.py
2. **Smaller Model**: Use yolov8n.pt or yolov8s.pt
3. **Reduce Resolution**: Modify window size in main.py
4. **Disable GUI**: Set `gui=False` in SumoSimulation

### For Better Detection
1. **Larger Model**: Use yolov8m.pt or yolov8l.pt
2. **Lower Threshold**: Set confidence_threshold to 0.3-0.4
3. **Enable Tracking**: Use `detect_with_tracking()` method

---

## Advanced Configuration

### Custom SUMO Network
To create your own traffic network:
1. Use SUMO's `netedit` tool
2. Save network as `data/sumo_config/custom.net.xml`
3. Create routes as `data/sumo_config/custom.rou.xml`
4. Update config in `data/sumo_config/custom.sumo.cfg`
5. Modify `src/main.py` to use your config file

### Different YOLOv8 Models
Available models (in order of speed → accuracy):
- `yolov8n.pt` - Nano (fastest, ~6MB)
- `yolov8s.pt` - Small (~22MB)
- `yolov8m.pt` - Medium (~52MB)
- `yolov8l.pt` - Large (~87MB)
- `yolov8x.pt` - Extra Large (slowest, most accurate, ~130MB)

Download any model:
```bash
python scripts/download_model.py --model yolov8m.pt
```

---

## Getting Help

If you encounter issues not covered here:
1. Check the [main README](README.md)
2. Review error messages carefully
3. Enable verbose logging in code
4. Open an issue on GitHub with:
   - Error message
   - System information
   - Steps to reproduce

## Next Steps

Once everything is running:
- Experiment with different SUMO networks
- Try different YOLOv8 models
- Modify detection thresholds
- Add custom visualization features
- Implement traffic analytics

Happy traffic monitoring! 🚗🚌🚛
