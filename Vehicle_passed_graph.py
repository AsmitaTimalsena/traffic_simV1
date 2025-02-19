import matplotlib.pyplot as plt
import numpy as np


simulation_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dedicated_lane_counts = [77, 91, 83, 89, 83, 79, 69, 60, 76, 72]
shared_lane_counts = [56, 59, 57, 65, 62, 64, 60, 66, 62, 58]


bar_width = 0.35
r1 = np.arange(len(simulation_number))
r2 = [x + bar_width for x in r1]


plt.figure(figsize=(10, 6))
plt.bar(r1, dedicated_lane_counts, width=bar_width, color='skyblue', label='Dedicated Lanes')
plt.bar(r2, shared_lane_counts, width=bar_width, color='lightgreen', label='Shared Lanes')

# Adding labels and title
plt.xlabel('Simulation Number (No of times simulation was run for span of 30 seconds for each scenario)')
plt.ylabel('Vehicles Passed')
plt.title('Comparison of Vehicles Passed in Dedicated vs Shared Lanes')
plt.xticks([r + bar_width / 2 for r in range(len(simulation_number))], simulation_number)
plt.legend()

plt.show()

#THe simulation data is as follows:
# 1.77,56
# 2.91,59
# 3.83,57
# 4.89,65
# 5.83,62
# 6.79,64
# 7.69,60
# 8.60,66
# 9.76,62
# 10.72,58