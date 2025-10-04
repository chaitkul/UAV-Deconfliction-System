# UAV Deconfliction in Shared Airspace

## Overview
This project implements a strategic deconfliction system for multiple drones operating in shared airspace. The system can:  

1. Check for spatial and temporal conflicts between planned flight missions.  
2. Simulate both random and hand-coded flight scenarios.  
3. Visualize drone trajectories in 2D and 3D.  

## Setup

### 1. Clone the repository
    git clone https://github.com/chaitkul/UAV-Deconfliction-System.git
    cd UAV-Deconfliction-System/

### 2. Install dependencies
    pip install -r requirements.txt

### 3. Usage
    python main.py

    This will:
        Generate both random and hand-coded flight scenarios.
        Run the deconfliction check for a primary flight against other flights.
        Show conflict status and details.
        Visualize flight trajectories in 2D and 3D.

### 4. Run Tests
    python -m pytest

    Tests cover:
        Conflict-free flights
        Single and multiple conflicts
        Edge cases
