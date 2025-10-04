import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from typing import List
from data_model import Flight
from trajectory import get_trajectory

# Function to plot 2D trajectories
def plot_2d_trajectories(flights: List[Flight]):
    """
    Plot 2D trajectories (x vs y) of multiple flights.
    """
    plt.figure(figsize=(8, 6))
    
    # Iterate through all flights
    for flight in flights:
        # Extract trajectory of the flight
        traj = get_trajectory(flight, time_step=1.0)
        xs = [pos[0] for _, pos in traj]
        ys = [pos[1] for _, pos in traj]
        plt.plot(xs, ys, marker='o', label=flight.flight_id)
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("2D Drone Trajectories")
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to animate 2D trajectories
def animate_2d(flights: List[Flight], time_step: float = 1.0, interval: int = 200):
    """
    Animate 2D flight positions over time.
    """
    
    # Compute trajectories for each flight
    traj_data = {f.flight_id: get_trajectory(f, time_step) for f in flights}
    max_len = max(len(traj) for traj in traj_data.values())
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Drone Flight Animation")
    
    # Initialize Line2D objects for each flight
    lines = {f.flight_id: ax.plot([], [], marker='o', label=f.flight_id)[0] for f in flights}
    ax.legend()

    # Frame update function
    def update(frame):
        for flight_id, traj in traj_data.items():
            # Extract x, y positions up to the current frame
            xs = [pos[0] for _, pos in traj[:frame+1]]
            ys = [pos[1] for _, pos in traj[:frame+1]]
            
            # Update the line's x and y data
            lines[flight_id].set_data(xs, ys)
        return lines.values()

    # Create the animation
    ani = FuncAnimation(fig, update, frames=max_len, interval=interval, blit=True)
    plt.show()

# Function to plot 3D trajectories
def plot_3d_trajectories(flights: List[Flight]):
    """
    Optional 3D trajectory plotting (x, y, z).
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Iterate through all flights
    for flight in flights:
        # Extract trajectory of the flight
        traj = get_trajectory(flight, time_step=1.0)
        xs = [pos[0] for _, pos in traj]
        ys = [pos[1] for _, pos in traj]
        zs = [pos[2] for _, pos in traj]
        ax.plot(xs, ys, zs, marker='o', label=flight.flight_id)
        
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Drone Trajectories")
    ax.legend()
    plt.show()

# Function to animate 3D trajectories
def animate_3d(flights: List[Flight], 
               time_step: float = 1.0, 
               interval: int = 200):
    """
    Animate 3D flight positions over time.
    """
    
    # Compute trajectories for each flight
    traj_data = {f.flight_id: get_trajectory(f, time_step) for f in flights}
    max_len = max(len(traj) for traj in traj_data.values())

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 20)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Drone Flight Animation")

    # Initialize Line3D objects for each flight
    lines = {f.flight_id: ax.plot([], [], [], marker='o', label=f.flight_id)[0] for f in flights}
    ax.legend()

    # Frame update function
    def update(frame):
        for flight_id, traj in traj_data.items():
            # Extract x, y, z positions up to the current frame
            xs = [pos[0] for _, pos in traj[:frame+1]]
            ys = [pos[1] for _, pos in traj[:frame+1]]
            zs = [pos[2] for _, pos in traj[:frame+1]]
            
            # Update the line's x, y and z data
            lines[flight_id].set_data(xs, ys)
            lines[flight_id].set_3d_properties(zs)
            
        return lines.values()

    # Create the animation
    ani = FuncAnimation(fig, update, frames=max_len, interval=interval, blit=True)
    plt.show()
