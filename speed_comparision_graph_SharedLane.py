import matplotlib.pyplot as plt
import numpy as np

# Time (in seconds)
time = list(range(30))  # 0 to 29 seconds

# Bike and car speed data extracted from your simulation
bike_speeds = [36.01, 36.17, 39.54, 39.54, 39.39, 38.26, 38.56, 38.56, 36.85, 38.56,
               38.56, 38.56, 38.56, 38.56, 38.56, 38.56, 36.78, 34.91, 36.52, 38.02,
               38.02, 38.02, 38.02, 38.02, 38.02, 38.02, 36.35, 38.02, 38.02, 38.02]

car_speeds = [29.60, 32.08, 32.08, 32.08, 32.08, 32.08, 32.08, 32.08, 32.08, 29.83,
              31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74,
              31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74, 31.74]

# Create the plot
plt.figure(figsize=(10, 5))

# Line plots with markers
plt.plot(time, bike_speeds, marker='o', linestyle='-', color='blue', label='Bike Speed')
plt.plot(time, car_speeds, marker='s', linestyle='-', color='red', label='Car Speed')

# Labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Speed (km/hr)')
plt.title('Speed Variation Over Time of four wheelers and bikes in Shared Lanes')
plt.legend()

# Adjust Y-axis ticks to show every integer speed (29, 30, 31, ...)
plt.yticks(np.arange(min(car_speeds + bike_speeds), max(car_speeds + bike_speeds) + 1, 1))

# Show grid for better readability
plt.grid(True, linestyle='--', alpha=0.5)

# Show the plot
plt.show()



"""
Value collected for shared lane for one particular simulation that is run for 30 seconds
pygame 2.6.1 (SDL 2.28.4, Python 3.13.0)
Hello from the pygame community. https://www.pygame.org/contribute.html
[Time: 00:00] Bike Avg Speed: 36.01 km/hr
[Time: 00:00] Car Avg Speed: 29.60 km/hr
[Time: 00:01] Bike Avg Speed: 36.17 km/hr
[Time: 00:01] Car Avg Speed: 32.08 km/hr
[Time: 00:02] Bike Avg Speed: 39.54 km/hr
[Time: 00:02] Car Avg Speed: 32.08 km/hr
[Time: 00:03] Bike Avg Speed: 39.54 km/hr
[Time: 00:03] Car Avg Speed: 32.08 km/hr
[Time: 00:04] Bike Avg Speed: 39.39 km/hr
[Time: 00:04] Car Avg Speed: 32.08 km/hr
[Time: 00:05] Bike Avg Speed: 38.26 km/hr
[Time: 00:05] Car Avg Speed: 32.08 km/hr
[Time: 00:06] Bike Avg Speed: 38.56 km/hr
[Time: 00:06] Car Avg Speed: 32.08 km/hr
[Time: 00:07] Bike Avg Speed: 38.56 km/hr
[Time: 00:07] Car Avg Speed: 32.08 km/hr
[Time: 00:08] Bike Avg Speed: 36.85 km/hr
[Time: 00:08] Car Avg Speed: 32.08 km/hr
[Time: 00:09] Bike Avg Speed: 38.56 km/hr
[Time: 00:09] Car Avg Speed: 29.83 km/hr
[Time: 00:10] Bike Avg Speed: 38.56 km/hr
[Time: 00:10] Car Avg Speed: 31.74 km/hr
[Time: 00:11] Bike Avg Speed: 38.56 km/hr
[Time: 00:11] Car Avg Speed: 31.74 km/hr
[Time: 00:12] Bike Avg Speed: 38.56 km/hr
[Time: 00:12] Car Avg Speed: 31.74 km/hr
[Time: 00:13] Bike Avg Speed: 38.56 km/hr
[Time: 00:13] Car Avg Speed: 31.74 km/hr
[Time: 00:14] Bike Avg Speed: 38.56 km/hr
[Time: 00:14] Car Avg Speed: 31.74 km/hr
[Time: 00:15] Bike Avg Speed: 38.56 km/hr
[Time: 00:15] Car Avg Speed: 31.74 km/hr
[Time: 00:16] Bike Avg Speed: 36.78 km/hr
[Time: 00:16] Car Avg Speed: 31.74 km/hr
[Time: 00:17] Bike Avg Speed: 34.91 km/hr
[Time: 00:17] Car Avg Speed: 31.74 km/hr
[Time: 00:18] Bike Avg Speed: 36.52 km/hr
[Time: 00:18] Car Avg Speed: 31.74 km/hr
[Time: 00:19] Bike Avg Speed: 38.02 km/hr
[Time: 00:19] Car Avg Speed: 31.74 km/hr
[Time: 00:20] Bike Avg Speed: 38.02 km/hr
[Time: 00:20] Car Avg Speed: 31.74 km/hr
[Time: 00:21] Bike Avg Speed: 38.02 km/hr
[Time: 00:21] Car Avg Speed: 31.74 km/hr
[Time: 00:22] Bike Avg Speed: 38.02 km/hr
[Time: 00:22] Car Avg Speed: 31.74 km/hr
[Time: 00:23] Bike Avg Speed: 38.02 km/hr
[Time: 00:23] Car Avg Speed: 31.74 km/hr
[Time: 00:24] Bike Avg Speed: 38.02 km/hr
[Time: 00:24] Car Avg Speed: 31.74 km/hr
[Time: 00:25] Bike Avg Speed: 38.02 km/hr
[Time: 00:25] Car Avg Speed: 31.74 km/hr
[Time: 00:26] Bike Avg Speed: 36.35 km/hr
[Time: 00:26] Car Avg Speed: 31.74 km/hr
[Time: 00:27] Bike Avg Speed: 38.02 km/hr
[Time: 00:27] Car Avg Speed: 31.74 km/hr
[Time: 00:28] Bike Avg Speed: 38.02 km/hr
[Time: 00:28] Car Avg Speed: 31.74 km/hr
[Time: 00:29] Bike Avg Speed: 38.02 km/hr
[Time: 00:29] Car Avg Speed: 31.74 km/hr
"""