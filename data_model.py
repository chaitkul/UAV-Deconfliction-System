from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime, timedelta

@dataclass
class Waypoint:
    """
    Represents a single waypoint in a drone mission.
    """
    x: float
    y: float
    z: Optional[float] = 0.0
    time_offset: Optional[float] = None

@dataclass
class MissionWindow:
    """
    Represents the overall time window during which a flight should occur.
    """
    start: datetime
    end: datetime

    def duration(self) -> float:
        """Returns mission duration in seconds."""
        return (self.end - self.start).total_seconds()

@dataclass
class Flight:
    """
    Represents a drone flight consisting of a series of waypoints.
    """
    flight_id: str
    waypoints: List[Waypoint]
    mission_window: MissionWindow

@dataclass
class Conflict:
    """
    Stores information about a detected conflict between two flights.
    """
    flight1_id: str
    flight2_id: str
    conflict_time: datetime
    location: Tuple[float, float, Optional[float]]
    distance: float
