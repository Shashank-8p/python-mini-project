import math
import sys
import time

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
except ImportError:
    print("❌ This project requires numpy and matplotlib.")
    print("Install them using: pip install numpy matplotlib")
    sys.exit(1)


GRAVITY = 9.81


def get_float(prompt, min_value=None, max_value=None):
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
            if min_value is not None and value < min_value:
                print(f"⚠️ Enter a value greater than or equal to {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"⚠️ Enter a value less than or equal to {max_value}.")
                continue
            return value
        except ValueError:
            print("⚠️ Invalid number. Try again.")


def projectile_stats(speed, angle_deg):
    angle_rad = math.radians(angle_deg)
    flight_time = (2 * speed * math.sin(angle_rad)) / GRAVITY
    max_height = (speed ** 2 * (math.sin(angle_rad) ** 2)) / (2 * GRAVITY)
    horizontal_range = (speed ** 2 * math.sin(2 * angle_rad)) / GRAVITY
    return flight_time, max_height, horizontal_range


def trajectory_points(speed, angle_deg, point_count=350):
    angle_rad = math.radians(angle_deg)
    flight_time, _, _ = projectile_stats(speed, angle_deg)

    if flight_time <= 0:
        return np.array([0.0]), np.array([0.0]), flight_time

    t = np.linspace(0, flight_time, point_count)
    x = speed * np.cos(angle_rad) * t
    y = speed * np.sin(angle_rad) * t - (0.5 * GRAVITY * t ** 2)
    y = np.maximum(y, 0)
    return x, y, flight_time


def show_plot(x, y):
    fig, ax = plt.subplots()
    max_limit = max(max(x), max(y)) * 1.1
    ax.set_xlim(0, max_limit)
    ax.set_ylim(0, max_limit)

    ax.set_title("Projectile Motion Simulator")
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Vertical Height (m)")
    ax.grid()
    line, = ax.plot([], [], color="#0078D7", linewidth=2.2, label="Projectile Path")
    point, = ax.plot([], [], 'ro')
    def update(frame):
        if frame >= len(x):
            return line, point
        line.set_data(x[:frame], y[:frame])
        point.set_data([x[frame-1]], [y[frame-1]])
        return line, point
    
    ani = FuncAnimation(fig, update, frames=len(x), interval=16, blit=False, repeat=False)
    
    plt.show()


def run_practice_mode():
    print("\n🎯 Projectile Calculator")
    speed = get_float("Enter launch speed (m/s): ", min_value=1)
    angle = get_float("Enter launch angle (degrees 1-89): ", min_value=1, max_value=89)

    print("\n⏳ Simulating trajectory...")
    time.sleep(0.6)

    x, y, _ = trajectory_points(speed, angle)
    flight_time, max_height, horizontal_range = projectile_stats(speed, angle)

    print("\n📊 Results")
    print(f"- TOF: {flight_time:.2f} s")
    print(f"- Hmax: {max_height:.2f} m")
    print(f"- Range: {horizontal_range:.2f} m")

    show_plot(x, y)


def main():
    print("🚀 Welcome to Projectile Motion Calculator 🚀")
    print("Compute TOF, Hmax, and Range\n")

    while True:
        print("Choose an option:")
        print("1) Calculate")
        print("2) Exit")

        choice = input("Enter choice (1-2): ").strip()

        if choice == "1":
            run_practice_mode()
        elif choice == "2":
            print("👋 Exiting... See you next launch!")
            sys.exit(0)
        else:
            print("⚠️ Invalid choice. Please pick 1 or 2.\n")


if __name__ == "__main__":
    main()