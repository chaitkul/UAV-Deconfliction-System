import random
from datetime import datetime, timedelta
from typing import List
from data_model import Flight, Waypoint, MissionWindow

# Function to generate random flight
def generate_random_flight(flight_id: str,
                           num_waypoints: int = 5,
                           x_range=(0, 100),
                           y_range=(0, 100),
                           z_range=(0, 20),
                           start_time: datetime = None,
                           duration: float = 300,
                           mode: str = "3d") -> Flight:
    """
    Generate a random flight in 2D or 3D.
    
    :param flight_id: unique flight ID
    :param num_waypoints: number of waypoints
    :param x_range: min/max X coordinates
    :param y_range: min/max Y coordinates
    :param z_range: min/max Z coordinates (altitude)
    :param start_time: mission start datetime
    :param duration: total mission duration in seconds
    :param mode: "2d" for 2D flight (z=0), "3d" for 3D flight
    :return: Flight object
    """
    
    # Initialize start time
    if start_time is None:
        start_time = datetime.now()
    
    # Compute end time and mission window
    end_time = start_time + timedelta(seconds=duration)
    mission_window = MissionWindow(start=start_time, end=end_time)

    # Store waypoints details based on dimension
    waypoints = []
    for i in range(num_waypoints):
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        z = 0 if mode == "2d" else random.uniform(*z_range)
        # Calculate time for each waypoint
        time_offset = i * (duration / (num_waypoints - 1))
        waypoints.append(Waypoint(x=x, y=y, z=z, time_offset=time_offset))
    
    return Flight(flight_id=flight_id, waypoints=waypoints, mission_window=mission_window)

def generate_handcoded_flight(flight_id: str, 
                              waypoints_data: List[tuple], 
                              start_time: datetime, 
                              duration: float,
                              mode: str = "3d") -> Flight:
    """
    Generate a hand-coded flight with specific waypoints in 2D or 3D.
    
    :param flight_id: unique flight ID
    :param waypoints_data: list of (x, y, z) tuples (z ignored if mode="2d")
    :param start_time: mission start datetime
    :param duration: total mission duration in seconds
    :param mode: "2d" for 2D flight (z=0), "3d" for 3D flight
    :return: Flight object
    """
    
    # Compute mission window
    mission_window = MissionWindow(start=start_time, end=start_time + timedelta(seconds=duration))
    num_waypoints = len(waypoints_data)

    # Store waypoints details based on dimension
    waypoints = []
    for i, (x, y, z) in enumerate(waypoints_data):
        z_val = 0 if mode == "2d" else z
        time_offset = i * (duration / (num_waypoints - 1))
        # Calculate time for each waypoint
        waypoints.append(Waypoint(x=x, y=y, z=z_val, time_offset=time_offset))

    return Flight(flight_id=flight_id, waypoints=waypoints, mission_window=mission_window)

# Function to generate a flight scenario
def generate_flight_scenario(num_flights: int = 3, 
                             start_time: datetime = None) -> List[Flight]:
    """
    Generate a scenario with multiple flights for testing.
    
    :param num_flights: number of flights to generate
    :param start_time: common start time
    :return: list of Flight objects
    """
    
    # List to store info of all flights
    flights = []
    for i in range(num_flights):
        # Generate random flight and store info
        flight = generate_random_flight(f"Flight_{i+1}", start_time=start_time)
        flights.append(flight)
    
    return flights