from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from data_model import Flight, Waypoint

# Function to interpolate position based on time
def linear_interp(p1: Waypoint, 
                  p2: Waypoint, 
                  t1: float, 
                  t2: float, 
                  t: float) -> Tuple[float, float, float]:
    """
    Linearly interpolate position between two waypoints for a given time t.
    
    :param p1: Start waypoint
    :param p2: End waypoint
    :param t1: Time of start waypoint (seconds)
    :param t2: Time of end waypoint (seconds)
    :param t: Target time to interpolate position (seconds)
    :return: (x, y, z) position at time t
    """
    
    # If start time and end time is equal, then return
    if t1 == t2:
        return (p1.x, p1.y, p1.z)
    
    # Calculate ratio of current time and interpolate
    ratio = (t - t1) / (t2 - t1)
    x = p1.x + ratio * (p2.x - p1.x)
    y = p1.y + ratio * (p2.y - p1.y)
    z = p1.z + ratio * (p2.z - p1.z)
    
    return (x, y, z)

# Function to compute position at a specific time
def get_position_at(flight: Flight, 
                    query_time: datetime) -> Optional[Tuple[float, float, float]]:
    """
    Get the interpolated position of a flight at a specific time.
    
    :param flight: Flight object
    :param query_time: datetime at which to query position
    :return: (x, y, z) position or None if query_time is outside mission window
    """
    
    # Convert query_time to seconds since mission start
    t_seconds = (query_time - flight.mission_window.start).total_seconds()
    
    # Ensure we have time offsets for waypoints
    waypoints = flight.waypoints
    times = [wp.time_offset if wp.time_offset is not None else idx for idx, wp in enumerate(waypoints)]
    
    # If outside mission window, return None
    if t_seconds < times[0] or t_seconds > times[-1]:
        return None
    
    # Find which waypoint segment contains query_time
    for i in range(len(waypoints) - 1):
        t1, t2 = times[i], times[i + 1]
        if t1 <= t_seconds <= t2:
            # Perform linear interpolation between these two waypoints
            return linear_interp(waypoints[i], waypoints[i + 1], t1, t2, t_seconds)
    
    # Return last waypoint to ensure we return a valid waypoint
    return (waypoints[-1].x, waypoints[-1].y, waypoints[-1].z)

# Function to get a trajectory as a list of positions
def get_trajectory(flight: Flight, 
                   time_step: float = 1.0) -> List[Tuple[datetime, Tuple[float, float, float]]]:
    """
    Generate a sampled trajectory for the flight.
    
    :param flight: Flight object
    :param time_step: time step in seconds
    :return: list of (datetime, (x, y, z))
    """
    
    # Empty list to store positions
    positions = []
    t = 0.0
    total_duration = flight.mission_window.duration()
    
    # Iterate until time is not out of bounds
    while t <= total_duration:
        query_time = flight.mission_window.start + timedelta(seconds=t)
        # Compute position for a flight at a particular time
        pos = get_position_at(flight, query_time)
        if pos:
            positions.append((query_time, pos))
        t += time_step
        
    return positions
