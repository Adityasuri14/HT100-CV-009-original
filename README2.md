# Grid Master — Smart Traffic Controller
**Project ID:** udbhav_004

Grid Master gives traffic lights real-time vision through computer vision and adaptive logic. Instead of fixed timers, intersections adjust to actual traffic conditions, with instant priority for emergency vehicles.

## What It Does
- Detects vehicles in real time using YOLOv8
- Calculates optimal green-light durations based on traffic density
- Gives immediate priority to ambulances
- Runs a full SUMO traffic simulation
- Displays live traffic state with a Pygame dashboard

## Tech Stack
- Python 3.8+
- YOLOv8 (Ultralytics)
- OpenCV
- SUMO
- Pygame

## Quick Start

Clone the repository:
```bash
git clone https://github.com/Udbhav2025/HT100-CV-009.git
cd HT100-CV-009
```

Setup:
**Windows**
```cmd
scripts\setup.bat
```

**Linux/macOS**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Generate the SUMO network:
```bash
scripts/generate_sumo_net.bat       # Windows
./sumo/generate_net.sh              # Linux/macOS
```

Run the system:
```bash
python main.py                  # Full system
python main.py --mode detector  # Detector only
python main.py --mode sumo      # SUMO only
```

## Configuration
Edit `config/config.yaml`:
```yaml
source:
  type: "video"  # or "camera"

traffic_control:
  base_green_duration: 10
  min_green_duration: 5
  max_green_duration: 60
```

## How It Works
1. YOLOv8 detects vehicles in each frame  
2. Counts are weighted to estimate traffic load  
3. The logic engine calculates the ideal green-light duration  
4. Ambulances trigger an immediate override  
5. SUMO simulates updated timings, and Pygame visualizes the state  

## Project Structure
```
src/          Core modules (detector, logic, SUMO, visualizer)
sumo/         SUMO network and routes
config/       Application settings
scripts/      Setup and helper scripts
main.py       Entry point
```

## Why It Matters
- Reduces congestion by adapting to real demand
- Helps emergency vehicles move faster and more safely
- Combines computer vision, simulation, and automation
- Easily extendable to real-world intersections

## Contributions
Feel free to fork the project and submit improvements.

# Built for Hackathon Innovation
Smarter cities begin with smarter traffic.
