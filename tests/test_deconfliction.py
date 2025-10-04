# tests/test_deconfliction.py
import pytest
from datetime import datetime, timedelta
# from data_model import Flight, Waypoint
from simulator import generate_handcoded_flight
from cli_api import check_mission

def test_conflict_free():
    """
    Test two flights that are far apart, expecting no conflicts.
    """
    start = datetime.now()
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,0,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(100,100,0), (110,100,0)], start, 10)

    # Check for conflicts with a 5 unit buffer using sampled mode
    status, conflicts = check_mission(flight1, [flight2], buffer=5.0, mode="sampled")
    assert status == "SAFE"
    assert len(conflicts) == 0

def test_single_conflict():
    """
    Test two flights that intersect, expecting a single conflict.
    """
    start = datetime.now()
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,10,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(10,0,0), (0,10,0)], start, 10)
    
    # Check with a smaller buffer to detect conflict
    status, conflicts = check_mission(flight1, [flight2], buffer=2.0, mode="sampled")
    assert status == "CONFLICT"
    assert len(conflicts) > 0

def test_multi_conflict():
    """
    Test multiple flights causing multiple conflicts.
    """
    start = datetime.now()
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,10,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(10,0,0), (0,10,0)], start, 10)
    flight3 = generate_handcoded_flight("F3", [(5,0,0), (5,10,0)], start, 10)

    # Check conflicts with two other flights
    status, conflicts = check_mission(flight1, [flight2, flight3], buffer=2.0, mode="sampled")
    assert status == "CONFLICT"
    assert len(conflicts) >= 2

# ------------------- EDGE CASES -------------------

def test_boundary_case():
    """
    Test flights just at the buffer limit, should not trigger conflict.
    """
    start = datetime.now()
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,0,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(0,5,0), (10,5,0)], start, 10)  # buffer=5

    # Using buffer equal to the distance between flights
    status, conflicts = check_mission(flight1, [flight2], buffer=5.0, mode="sampled")
    # Exactly at buffer, consider SAFE
    assert status == "SAFE"
    assert len(conflicts) == 0

def test_non_overlapping_time_windows():
    """Flights occupy the same space but at different times: should be SAFE."""
    start = datetime.now()
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,0,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(0,0,0), (10,0,0)], start + timedelta(seconds=20), 10)
    status, conflicts = check_mission(flight1, [flight2], buffer=5.0, mode="sampled")
    assert status == "SAFE"
    assert len(conflicts) == 0

def test_missing_time_offsets():
    """Waypoints without explicit time offsets are handled correctly."""
    start = datetime.now()
    # Waypoints with time_offset=None
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,0,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(0,5,0), (10,5,0)], start, 10)
    # Remove time_offset manually
    for wp in flight1.waypoints + flight2.waypoints:
        wp.time_offset = None
    status, conflicts = check_mission(flight1, [flight2], buffer=2.0, mode="sampled")
    assert status == "SAFE"
    assert len(conflicts) == 0

def test_simultaneous_start_or_end():
    """Flights starting or ending at the same moment are checked accurately."""
    start = datetime.now()
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,0,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(0,5,0), (10,5,0)], start, 10)
    status, conflicts = check_mission(flight1, [flight2], buffer=2.0, mode="sampled")
    assert status == "SAFE"
    assert len(conflicts) == 0

def test_altitude_only_conflict():
    """Flights separated in XY but too close in Z should trigger a conflict."""
    start = datetime.now()
    flight1 = generate_handcoded_flight("F1", [(0,0,0), (10,0,0)], start, 10)
    flight2 = generate_handcoded_flight("F2", [(0,0,1), (10,0,1)], start, 10)
    status, conflicts = check_mission(flight1, [flight2], buffer=2.0, mode="sampled")
    assert status == "CONFLICT"
    assert len(conflicts) > 0