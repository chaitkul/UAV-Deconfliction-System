from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from data_model import Flight, Conflict
from trajectory import get_position_at

# Function to calculate distance between 2 points
def euclidean_distance(p1, p2) -> float:
    """Compute 3D Euclidean distance between two points."""
    return np.sqrt((p1[0] - p2[0])**2 +
                   (p1[1] - p2[1])**2 +
                   (p1[2] - p2[2])**2)

def check_conflicts_sampled(primary: Flight, 
                            others: List[Flight], 
                            buffer: float, 
                            time_step: float = 1.0) -> List[Conflict]:
    """
    Detect conflicts using sampled positions at discrete time steps.
    
    :param primary: primary flight to check
    :param others: list of other flights
    :param buffer: minimum allowed separation distance
    :param time_step: seconds between sampled positions
    :return: list of Conflict objects
    """
    
    # List to store conflicts, if any
    conflicts = []
    
    # Compute total duration of flight
    total_duration = primary.mission_window.duration()
    t = 0.0
    
    # Go through entire time duration to check conflicts
    while t <= total_duration:
        current_time = primary.mission_window.start + timedelta(seconds=t)
        # Get position of primary flight
        primary_pos = get_position_at(primary, current_time)
        if not primary_pos:
            t += time_step
            continue

        # Iterate through all other flights
        for other in others:
            # Get position of other flights
            other_pos = get_position_at(other, current_time)
            if not other_pos:
                continue

            # Compute distance between primary flight and other flights
            distance = euclidean_distance(primary_pos, other_pos)
            # If distance is less than buffer, consider it as a conflict
            if distance < buffer:
                conflicts.append(Conflict(
                    flight1_id=primary.flight_id,
                    flight2_id=other.flight_id,
                    conflict_time=t,
                    location=primary_pos,
                    distance=distance
                ))
        
        # Increase time step
        t += time_step
        
    return conflicts


def closest_approach_linear(p1_start: Tuple[float, float, float], 
                            p1_end: Tuple[float, float, float], 
                            t1_start: float, 
                            t1_end: float, 
                            p2_start: Tuple[float, float, float], 
                            p2_end: Tuple[float, float, float], 
                            t2_start: float, 
                            t2_end: float) -> Tuple[Optional[float], Optional[float]]:
    """
    Analytically compute closest approach distance between two linear segments with time interpolation.
    Returns (closest_distance, time_at_closest).
    """
    
    # Convert positions and times to numpy arrays
    p1_start, p1_end, p2_start, p2_end = map(np.array, [p1_start, p1_end, p2_start, p2_end])
    
    # Constant velocities for each segment
    v1 = (p1_end - p1_start) / (t1_end - t1_start)
    v2 = (p2_end - p2_start) / (t2_end - t2_start)
    
    # Time window where the two flights are both active
    dt_start = max(t1_start, t2_start)
    dt_end = min(t1_end, t2_end)
    if dt_start >= dt_end:
        # No overlapping time, no conflict possible
        return None, None

    # Minimize ||(p1 + v1*t) - (p2 + v2*t)||^2
    # Relative velocity and position at dt_start
    v_rel = v1 - v2
    p_rel = (p1_start + v1*(dt_start - t1_start)) - (p2_start + v2*(dt_start - t2_start))
    
    # Solve for t_closest that minimizes distance
    # distance^2 = || p_rel + v_rel * t ||^2
    t_closest = -np.dot(p_rel, v_rel) / np.dot(v_rel, v_rel) if np.dot(v_rel, v_rel) > 0 else 0
    t_closest = np.clip(t_closest, 0, dt_end - dt_start)
    
    # Positions of both flights at the closest approach
    closest_point1 = p1_start + v1*(dt_start - t1_start + t_closest)
    closest_point2 = p2_start + v2*(dt_start - t2_start + t_closest)
    
    # Distance at that time
    distance = np.linalg.norm(closest_point1 - closest_point2)
    
    # Time when this happens
    time_at_closest = dt_start + t_closest
    
    return distance, time_at_closest

def check_conflicts_analytic(primary: Flight, 
                             others: List[Flight], 
                             buffer: float) -> List[Conflict]:
    """
    Detect conflicts analytically for linear segments between waypoints.
    Works for 2D or 3D flights based on available attributes (x, y[, z]).
    """
    
    conflicts = []
    
    # Extract waypoints and times for primary flight
    primary_wp = primary.waypoints
    primary_times = [wp.time_offset if wp.time_offset is not None else idx for idx, wp in enumerate(primary_wp)]
    
    for other in others:
        other_wp = other.waypoints
        other_times = [wp.time_offset if wp.time_offset is not None else idx for idx, wp in enumerate(other_wp)]
        
        # Compare each segment of primary with each segment of the other flight
        for i in range(len(primary_wp) - 1):
            for j in range(len(other_wp) - 1):

                # Extract coordinates
                def get_coords(wp):
                    if hasattr(wp, 'z'):
                        return np.array([wp.x, wp.y, wp.z], dtype=float)
                    else:
                        return np.array([wp.x, wp.y], dtype=float)

                p1_start = get_coords(primary_wp[i])
                p1_end   = get_coords(primary_wp[i+1])
                p2_start = get_coords(other_wp[j])
                p2_end   = get_coords(other_wp[j+1])

                # Call analytic closest-approach
                dist, t_closest = closest_approach_linear(
                    p1_start, p1_end, primary_times[i], primary_times[i+1],
                    p2_start, p2_end, other_times[j], other_times[j+1]
                )

                # Check if this segment pair creates a conflict
                if dist is not None and dist < buffer:
                    conflict_time = primary.mission_window.start + timedelta(seconds=t_closest)
                    conflicts.append(Conflict(
                        flight1_id=primary.flight_id,
                        flight2_id=other.flight_id,
                        conflict_time=t_closest,
                        location=get_position_at(primary, conflict_time),
                        distance=dist
                    ))
                    
    return conflicts

