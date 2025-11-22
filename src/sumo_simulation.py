#!/usr/bin/env python3
"""
SUMO Simulation Handler
Manages SUMO traffic simulation using TraCI API.
"""

import os
import sys
import traci
import numpy as np
from PIL import Image
from pathlib import Path


class SumoSimulation:
    """
    Handles SUMO simulation initialization, stepping, and data retrieval.
    """
    
    def __init__(self, config_file, gui=True, port=8813):
        """
        Initialize SUMO simulation.
        
        Args:
            config_file (str): Path to SUMO configuration file (.sumocfg)
            gui (bool): Whether to use SUMO GUI (True) or command-line version (False)
            port (int): TraCI connection port
        """
        self.config_file = config_file
        self.gui = gui
        self.port = port
        self.connected = False
        
        # Validate SUMO installation
        self._check_sumo_installation()
        
        # Start SUMO
        self._start_sumo()
        
    def _check_sumo_installation(self):
        """Check if SUMO is properly installed and SUMO_HOME is set."""
        if 'SUMO_HOME' not in os.environ:
            raise EnvironmentError(
                "SUMO_HOME environment variable not set. "
                "Please install SUMO and set SUMO_HOME to the installation directory."
            )
        
        sumo_home = os.environ['SUMO_HOME']
        if not os.path.exists(sumo_home):
            raise FileNotFoundError(
                f"SUMO_HOME points to non-existent directory: {sumo_home}"
            )
        
        # Add SUMO tools to Python path
        tools = os.path.join(sumo_home, 'tools')
        if tools not in sys.path:
            sys.path.append(tools)
    
    def _start_sumo(self):
        """Start SUMO simulation with TraCI."""
        # Check if config file exists
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"SUMO config file not found: {self.config_file}")
        
        # Determine SUMO binary
        sumo_binary = "sumo-gui" if self.gui else "sumo"
        
        # SUMO command with options
        sumo_cmd = [
            sumo_binary,
            "-c", self.config_file,
            "--start",  # Start simulation immediately
            "--quit-on-end",  # Close SUMO when simulation ends
            "--step-length", "0.1",  # Simulation step length in seconds
            "--delay", "50",  # Delay between steps (ms) for GUI
        ]
        
        try:
            # Start SUMO with TraCI
            traci.start(sumo_cmd, port=self.port)
            self.connected = True
            print(f"  → TraCI connected on port {self.port}")
            
            # Get simulation info
            num_vehicles = traci.vehicle.getIDCount()
            print(f"  → Initial vehicles: {num_vehicles}")
            
        except Exception as e:
            raise ConnectionError(f"Failed to start SUMO simulation: {e}")
    
    def step(self):
        """
        Advance simulation by one step.
        
        Returns:
            bool: True if simulation is still running, False if ended
        """
        if not self.connected:
            return False
        
        try:
            traci.simulationStep()
            
            # Check if simulation has ended
            min_expected_vehicles = traci.simulation.getMinExpectedNumber()
            if min_expected_vehicles <= 0:
                return False
            
            return True
            
        except traci.exceptions.FatalTraCIError:
            self.connected = False
            return False
    
    def get_screenshot(self):
        """
        Capture a screenshot from SUMO GUI.
        
        Returns:
            numpy.ndarray: Screenshot as RGB image array, or None if capture fails
        """
        if not self.connected or not self.gui:
            return None
        
        try:
            # Get the default view
            view_id = traci.gui.getIDList()[0] if traci.gui.getIDCount() > 0 else 'View #0'
            
            # Create temporary screenshot file
            temp_file = "temp_screenshot.png"
            
            # Capture screenshot
            traci.gui.screenshot(view_id, temp_file)
            
            # Load screenshot
            if os.path.exists(temp_file):
                img = Image.open(temp_file)
                img_array = np.array(img)
                
                # Clean up temporary file
                os.remove(temp_file)
                
                return img_array
            else:
                return None
                
        except Exception as e:
            print(f"Warning: Failed to capture screenshot: {e}")
            return None
    
    def get_vehicle_ids(self):
        """
        Get list of all vehicle IDs currently in simulation.
        
        Returns:
            list: List of vehicle ID strings
        """
        if not self.connected:
            return []
        
        try:
            return traci.vehicle.getIDList()
        except Exception:
            return []
    
    def get_vehicle_position(self, vehicle_id):
        """
        Get position of a specific vehicle.
        
        Args:
            vehicle_id (str): Vehicle ID
            
        Returns:
            tuple: (x, y) position, or None if not available
        """
        if not self.connected:
            return None
        
        try:
            return traci.vehicle.getPosition(vehicle_id)
        except Exception:
            return None
    
    def get_vehicle_speed(self, vehicle_id):
        """
        Get speed of a specific vehicle.
        
        Args:
            vehicle_id (str): Vehicle ID
            
        Returns:
            float: Speed in m/s, or None if not available
        """
        if not self.connected:
            return None
        
        try:
            return traci.vehicle.getSpeed(vehicle_id)
        except Exception:
            return None
    
    def get_vehicle_type(self, vehicle_id):
        """
        Get type of a specific vehicle.
        
        Args:
            vehicle_id (str): Vehicle ID
            
        Returns:
            str: Vehicle type, or None if not available
        """
        if not self.connected:
            return None
        
        try:
            return traci.vehicle.getTypeID(vehicle_id)
        except Exception:
            return None
    
    def get_simulation_time(self):
        """
        Get current simulation time.
        
        Returns:
            float: Simulation time in seconds
        """
        if not self.connected:
            return 0.0
        
        try:
            return traci.simulation.getTime()
        except Exception:
            return 0.0
    
    def close(self):
        """Close SUMO simulation and TraCI connection."""
        if self.connected:
            try:
                traci.close()
                self.connected = False
            except Exception as e:
                print(f"Warning: Error closing TraCI connection: {e}")
