import pygame
import sys
import time


pygame.init()


# Screen dimensions
screen_width = 1280
screen_height = 800


# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))


background_image = pygame.image.load("dedicated_laneIMG.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


pygame.display.set_caption("Pygame with Background Image")


dash_coordinates = [
    # Traffic lights
    # north road
    (760, 420), (680, 420),
    # East road
    (880, 590),
    # South road
    (600, 690),
    # West road
    (400, 520),
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
    [(400, 520)],  # West
]

for coord in directions[current_green_index]:
    dash_colors[coord] = (0, 255, 0)  # Set the first direction's lights to green


color_change_time = 10000  # Time interval in milliseconds
last_color_change = pygame.time.get_ticks()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Get the current time
    current_time = pygame.time.get_ticks()


    # Change traffic light colors every 5 seconds
    if current_time - last_color_change >= color_change_time:
        # Reset all lights to red
        for coord in dash_colors:
            dash_colors[coord] = (255, 0, 0)
        # Set the current direction to green
        current_green_index = (current_green_index + 1) % len(directions)
        for coord in directions[current_green_index]:
            dash_colors[coord] = (0, 255, 0)
        # Update the last color change time
        last_color_change = current_time




    # Draw the background and traffic lights
    screen.blit(background_image, (0, 0))
   

    for (x, y) in dash_coordinates:
        if x == 880 or x == 400:  # East and West roads (vertical dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x, y - dash_length // 2), (x, y + dash_length // 2), dash_thickness)
        else:  # North and South roads (horizontal dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x - dash_length // 2, y), (x + dash_length // 2, y), dash_thickness)


    pygame.display.flip()


pygame.quit()
sys.exit()


