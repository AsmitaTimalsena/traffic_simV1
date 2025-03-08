import matplotlib.pyplot as plt
import numpy as np

# Simulation data
simulation_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dedicated_lane_collision_counts = [1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
shared_lane_collision_counts = [2, 4, 8, 2, 3, 0, 7, 3, 1, 4]

# Bar chart parameters
bar_width = 0.35
r1 = np.arange(len(simulation_number))
r2 = [x + bar_width for x in r1]

# Plotting the bar graph
plt.figure(figsize=(10, 6))
plt.bar(r1, dedicated_lane_collision_counts, width=bar_width, color='skyblue', label='Dedicated Lanes')
plt.bar(r2, shared_lane_collision_counts, width=bar_width, color='lightgreen', label='Shared Lanes')

# Labels and title
plt.xlabel('Simulation Number (No of times simulation was run for span of 1 minute for each scenario)')
plt.ylabel('Collision Counts')
plt.title('Comparison of Collision Counts in Dedicated vs Shared Lanes')
plt.xticks([r + bar_width / 2 for r in range(len(simulation_number))], simulation_number)
plt.legend()

# Display the plot
plt.show()


#THe simulation data is as follows:
# 1.0,2
# 2. 0, 4
# 3.1 , 8
# 4. 0, 2
# 5. 1, 3
# 6. 0, 0
# 7. 1, 7
# 8. 1, 3
# 9. 0,1
# 10.1 ,4