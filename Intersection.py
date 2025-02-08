
'''
Requirements:
Speed of vehicles must be random:
 self.speed = random.uniform(2.5, 4.0) if vehicle_type == "motorcycle" else random.uniform(1.5, 3.0)

 Size of each vehicle must be random:
  # Vehicle size
        if vehicle_type == "motorcycle":
            self.width = random.randint(8, 12)  # Narrower width for a sleek look
            self.height = random.randint(22, 28)  # Taller height for elongation
        elif vehicle_type == "car":
            self.width = random.randint(20, 30)  # Width for cars
            self.height = random.randint(40, 50)  # Length for cars

    Also, the speed of vehicles both cars/bikes can increase if there is no vehicle ahead.
'''



import pygame
import random
import sys

pygame.init()


screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("North Road Vehicle Simulation")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


background_image = pygame.image.load("dedicated_laneIMG.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

total_vehicles_passed = 0
motorcycle_positions = [760, 795]
car_positions = [680, 850]     
motorcycle_safe_threshold = 50  
car_safe_threshold = 180  
max_vehicles_per_lane = 20 

dash_coordinates = [
    # Traffic lights
    # north road
    (760, 420), (680, 420),
    # East road
    (880, 590),
    # South road
    (600, 690),
    # West road
    (400, 600),
]

dash_length = 20  # Length of the dash
dash_thickness = 5  # Thickness of the dash

# Initial color for traffic lights
dash_colors = {coord: (255, 0, 0) for coord in dash_coordinates}  # Red initially
current_green_index = 0

directions = [
    [(760, 420), (680, 420)],  # North
    [(600, 690)],  # South
    [(880, 590)],  # East
    [(400, 600)],  # West
]

for coord in directions[current_green_index]:
    dash_colors[coord] = (0, 255, 0)  # Set the first direction's lights to green

# Traffic light timings
green_time = 27000  # 27 seconds
orange_time = 3000  # 3 seconds
total_time = green_time + orange_time  # Total time for each direction

# West direction has different timings
west_green_time = 12000  # 12 seconds
west_orange_time = 3000  # 3 seconds
west_total_time = west_green_time + west_orange_time  # Total time for west direction

last_color_change = pygame.time.get_ticks()



# Create vehicles for each lane
vehicles = {pos: [] for pos in motorcycle_positions + car_positions}


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    # Get the current time
    current_time = pygame.time.get_ticks()

    # Change traffic light colors based on timings
    if current_time - last_color_change >= total_time:
        # Reset all lights to red
        for coord in dash_colors:
            dash_colors[coord] = (255, 0, 0)
        # Set the current direction to green
        current_green_index = (current_green_index + 1) % len(directions)
        for coord in directions[current_green_index]:
            dash_colors[coord] = (0, 255, 0)
        # Update the last color change time
        last_color_change = current_time
    elif current_time - last_color_change >= green_time:
        # Set the current direction to orange
        for coord in directions[current_green_index]:
            dash_colors[coord] = (255, 165, 0)

    # Special logic for the west road
    if current_green_index == 3:  # West road is active
        if current_time - last_color_change >= west_green_time + west_orange_time:
            # Reset all lights to red
            for coord in dash_colors:
                dash_colors[coord] = (255, 0, 0)
            # Set the next direction to green
            current_green_index = (current_green_index + 1) % len(directions)
            for coord in directions[current_green_index]:
                dash_colors[coord] = (0, 255, 0)
            # Update the last color change time
            last_color_change = current_time
        elif current_time - last_color_change >= west_green_time:
            # Set the west road to orange
            for coord in directions[current_green_index]:
                dash_colors[coord] = (255, 165, 0)

    # Draw the background and traffic lights
    screen.blit(background_image, (0, 0))

    for (x, y) in dash_coordinates:
        if x == 880 or x == 400:  # East and West roads (vertical dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x, y - dash_length // 2), (x, y + dash_length // 2), dash_thickness)
        else:  # North and South roads (horizontal dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x - dash_length // 2, y), (x + dash_length // 2, y), dash_thickness)

    
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Adjust frame rate for smoother simulation

pygame.quit()
sys.exit()