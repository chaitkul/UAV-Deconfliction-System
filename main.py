from datetime import datetime
from simulator import generate_random_flight, generate_handcoded_flight
from cli_api import check_mission
from visualize import plot_2d_trajectories, animate_2d, plot_3d_trajectories, animate_3d

def run_scenario(flights, buffer_distance=5.0, mode="analytic", title="Scenario", dimension="3d"):
    """
    Run a flight scenario (2D or 3D): check for conflicts, print results, and visualize.
    :param flights: list of Flight objects
    :param buffer_distance: conflict buffer in meters
    :param mode: conflict checking mode
    :param title: scenario title
    :param dimension: "2d" or "3d"
    """
    
    # Initialize primary flight and other flights
    primary_flight = flights[0]
    other_flights = flights[1:]

    print(f"\n--- {title} ---")
    print("Flights:")

    for f in flights:
        if dimension == "2d":
            print(f.flight_id, [(wp.x, wp.y) for wp in f.waypoints])
        else:
            print(f.flight_id, [(wp.x, wp.y, wp.z) for wp in f.waypoints])

    # Check conflicts
    status, conflicts = check_mission(primary_flight, other_flights, buffer=buffer_distance, mode=mode)
    print(f"\nMission Status for {primary_flight.flight_id}: {status}")

    # Print conflict details, if any
    if conflicts:
        print("Conflicts detected:")
        for c in conflicts:
            print(f"- With {c.flight2_id} at {c.conflict_time}, distance {c.distance:.2f}m, location {c.location}")
    else:
        print("No conflicts detected.")

    # Visualization
    if dimension == "2d":
        animate_2d(flights)
        plot_2d_trajectories(flights)
    else:
        animate_3d(flights)
        plot_3d_trajectories(flights)


def main():
    start_time = datetime.now()

    # 2D SAFE scenario
    safe_2d_flights = [
        generate_handcoded_flight("F1", [(0,0,0), (10,0,0)], start_time, duration=10, mode="2d"),
        generate_handcoded_flight("F2", [(0,10,0), (10,10,0)], start_time, duration=10, mode="2d"),
        generate_handcoded_flight("F3", [(0,20,0), (10,20,0)], start_time, duration=10, mode="2d"),
    ]
    run_scenario(safe_2d_flights, buffer_distance=5.0, title="2D Safe Scenario (Handcoded)", dimension='2d')

    # 2D CONFLICT scenario (handcoded)
    conflict_2d_flights = [
        generate_handcoded_flight("F1", [(0,0,0), (10,10,0)], start_time, duration=10, mode="2d"),
        generate_handcoded_flight("F2", [(10,0,0), (0,10,0)], start_time, duration=10, mode="2d"),
        generate_handcoded_flight("F3", [(5,0,0), (5,10,0)], start_time, duration=10, mode="2d"),
    ]
    run_scenario(conflict_2d_flights, buffer_distance=2.0, title="2D Conflict Scenario", dimension='2d')

    # 2D Random scenario
    safe_2d_flights = [generate_random_flight(f"F{i+1}", mode="2d", start_time=start_time) for i in range(3)]
    run_scenario(safe_2d_flights, buffer_distance=5.0, title="2D Random Scenario", dimension='2d')

    # 3D SAFE scenario
    safe_3d_flights = [
        generate_handcoded_flight("F1", [(0,0,0), (10,0,5)], start_time, duration=10, mode="3d"),
        generate_handcoded_flight("F2", [(0,10,10), (10,10,15)], start_time, duration=10, mode="3d"),
        generate_handcoded_flight("F3", [(0,20,20), (10,20,25)], start_time, duration=10, mode="3d"),
    ]
    run_scenario(safe_3d_flights, buffer_distance=5.0, title="3D Safe Scenario (Handcoded)", dimension='3d')
    
    # 3D CONFLICT scenario (handcoded)
    conflict_3d_flights = [
        generate_handcoded_flight("F1", [(0,0,0), (10,10,5)], start_time, duration=10, mode="3d"),
        generate_handcoded_flight("F2", [(10,0,0), (0,10,5)], start_time, duration=10, mode="3d"),
        generate_handcoded_flight("F3", [(5,0,2), (5,10,2)], start_time, duration=10, mode="3d"),
    ]
    run_scenario(conflict_3d_flights, buffer_distance=2.0, title="3D Conflict Scenario", dimension='3d')

    # 3D Random scenario
    safe_3d_flights = [generate_random_flight(f"F{i+1}", mode="3d", start_time=start_time) for i in range(3)]
    run_scenario(safe_3d_flights, buffer_distance=5.0, title="3D Random Scenario", dimension='3d')

if __name__ == "__main__":
    main()
