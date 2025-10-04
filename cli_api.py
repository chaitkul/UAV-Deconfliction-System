from typing import List, Tuple
from data_model import Flight, Conflict
from collision_check import check_conflicts_sampled, check_conflicts_analytic

# Function to check if any conflicts exist
def check_mission(primary_flight: Flight, 
                  other_flights: List[Flight], 
                  buffer: float, 
                  mode: str = "sampled", 
                  time_step: float = 1.0) -> Tuple[str, List[Conflict]]:
    """
    Main interface to check a mission for conflicts.
    
    :param primary_flight: the flight to be executed
    :param other_flights: list of other flights in the airspace
    :param buffer: minimum separation distance in meters
    :param mode: "sampled" or "analytic"
    :param time_step: time step for sampled mode
    :return: tuple (status, list of conflicts)
    """
    
    # Check conflicts using sampling or analytical method
    if mode == "sampled":
        conflicts = check_conflicts_sampled(primary_flight, other_flights, buffer, time_step)
    elif mode == "analytic":
        conflicts = check_conflicts_analytic(primary_flight, other_flights, buffer)
    else:
        raise ValueError("Mode must be 'sampled' or 'analytic'")
    
    status = "SAFE" if len(conflicts) == 0 else "CONFLICT"
    return status, conflicts
