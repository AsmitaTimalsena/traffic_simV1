import matplotlib.pyplot as plt
import numpy as np

# Time (in seconds)
time = list(range(31))  # 0 to 30 seconds

# Bike and car speed data
bike_speeds = [39.00, 40.01, 41.00, 40.10, 42.01, 42.01, 42.01, 46.03, 45.27, 50.54,
               51.04, 41.83, 46.77, 41.30, 41.13, 45.14, 46.47, 44.52, 42.45, 44.34,
               42.30, 48.29, 45.56, 46.40, 40.07, 39.97, 39.53, 43.39, 38.66, 41.95, 41.43]

car_speeds = [30.24, 31.00, 28.63, 28.63, 28.63, 28.63, 28.63, 28.63, 32.90, 32.90,
              32.90, 32.90, 32.90, 32.13, 32.13, 32.13, 32.52, 32.52, 32.90, 32.90,
              33.44, 33.44, 33.82, 35.12, 35.51, 36.92, 34.91, 34.73, 34.73, 33.82, 33.82]

# Create the plot
plt.figure(figsize=(10, 5))

# Line plots with markers
plt.plot(time, bike_speeds, marker='o', linestyle='-', color='blue', label='Bike Speed')
plt.plot(time, car_speeds, marker='s', linestyle='-', color='red', label='Car Speed')

# Labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Speed (km/hr)')
plt.title('Speed Variation Over Time of four wheelers and bikes in  Dedicated Lanes')
plt.legend()

# Adjust Y-axis ticks to show every 5 units instead of every 1
min_speed = 0  # Start from 0
max_speed = 55  # Round up to nearest 5 above max speed
plt.yticks(np.arange(min_speed, max_speed, 5))  # Step of 5 units

# Show grid for better readability
plt.grid(True, linestyle='--', alpha=0.5)

# Show the plot
plt.show()
"""
Value collected for dedicated lane for one particular simulation that is run for 30 seconds
pygame 2.6.1 (SDL 2.28.4, Python 3.13.0)
Hello from the pygame community. https://www.pygame.org/contribute.html
Time 00:01 - Car Avg Speed: 0.00 km/hr, Bike Avg Speed: 0.00 km/hr
Time 00:02 - Car Avg Speed: 0.00 km/hr, Bike Avg Speed: 0.00 km/hr
Time 00:03 - Car Avg Speed: 28.63 km/hr, Bike Avg Speed: 0.00 km/hr
Time 00:04 - Car Avg Speed: 28.63 km/hr, Bike Avg Speed: 0.00 km/hr
Time 00:05 - Car Avg Speed: 28.63 km/hr, Bike Avg Speed: 42.01 km/hr
Time 00:06 - Car Avg Speed: 28.63 km/hr, Bike Avg Speed: 42.01 km/hr
Time 00:07 - Car Avg Speed: 28.63 km/hr, Bike Avg Speed: 42.01 km/hr
Time 00:08 - Car Avg Speed: 28.63 km/hr, Bike Avg Speed: 46.03 km/hr
Time 00:09 - Car Avg Speed: 32.90 km/hr, Bike Avg Speed: 45.27 km/hr
Time 00:10 - Car Avg Speed: 32.90 km/hr, Bike Avg Speed: 50.54 km/hr
Time 00:11 - Car Avg Speed: 32.90 km/hr, Bike Avg Speed: 51.04 km/hr
Time 00:12 - Car Avg Speed: 32.90 km/hr, Bike Avg Speed: 41.83 km/hr
Time 00:13 - Car Avg Speed: 32.90 km/hr, Bike Avg Speed: 46.77 km/hr
Time 00:14 - Car Avg Speed: 32.13 km/hr, Bike Avg Speed: 41.30 km/hr
Time 00:15 - Car Avg Speed: 32.13 km/hr, Bike Avg Speed: 41.13 km/hr
Time 00:16 - Car Avg Speed: 32.13 km/hr, Bike Avg Speed: 45.14 km/hr
Time 00:17 - Car Avg Speed: 32.52 km/hr, Bike Avg Speed: 46.47 km/hr
Time 00:18 - Car Avg Speed: 32.52 km/hr, Bike Avg Speed: 44.52 km/hr
Time 00:19 - Car Avg Speed: 32.90 km/hr, Bike Avg Speed: 42.45 km/hr
Time 00:20 - Car Avg Speed: 32.90 km/hr, Bike Avg Speed: 44.34 km/hr
Time 00:21 - Car Avg Speed: 33.44 km/hr, Bike Avg Speed: 42.30 km/hr
Time 00:22 - Car Avg Speed: 33.44 km/hr, Bike Avg Speed: 48.29 km/hr
Time 00:23 - Car Avg Speed: 33.82 km/hr, Bike Avg Speed: 45.56 km/hr
Time 00:24 - Car Avg Speed: 35.12 km/hr, Bike Avg Speed: 46.40 km/hr
Time 00:25 - Car Avg Speed: 35.51 km/hr, Bike Avg Speed: 40.07 km/hr
Time 00:26 - Car Avg Speed: 36.92 km/hr, Bike Avg Speed: 39.97 km/hr
Time 00:27 - Car Avg Speed: 34.91 km/hr, Bike Avg Speed: 39.53 km/hr
Time 00:28 - Car Avg Speed: 34.73 km/hr, Bike Avg Speed: 43.39 km/hr
Time 00:29 - Car Avg Speed: 34.73 km/hr, Bike Avg Speed: 38.66 km/hr
Time 00:30 - Car Avg Speed: 33.82 km/hr, Bike Avg Speed: 41.95 km/hr
Time 00:31 - Car Avg Speed: 33.82 km/hr, Bike Avg Speed: 41.43 km/hr
"""