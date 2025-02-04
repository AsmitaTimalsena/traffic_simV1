import pygame
import sys

pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 800

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.image.load("dedicated_laneIMG.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

pygame.display.set_caption("Traffic Light Simulation")

# Traffic light coordinates
dash_coordinates = {
    "north": [(760, 420), (680, 420)],
    "south": [(600, 690)],
    "east": [(880, 590)],
    "west": [(400, 600)],
}

# Traffic light color dictionary
dash_colors = {coord: (255, 0, 0) for coords in dash_coordinates.values() for coord in coords}  # Initially all red

# Traffic light sequence with time intervals
traffic_cycle = [
    ("north", 30000),  # North green for 30 seconds
    ("south", 30000),  # South green for 15 seconds
    ("east", 30000),   # East green for 30s
    ("west", 15000),   # West green for 15s
]

# Timer and index initialization
current_phase = 0
phase_start_time = pygame.time.get_ticks()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current time
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - phase_start_time

    # Get current phase details
    current_direction, phase_duration = traffic_cycle[current_phase]

    # Change phase if duration is over
    if elapsed_time >= phase_duration:
        phase_start_time = current_time  # Reset timer
        current_phase = (current_phase + 1) % len(traffic_cycle)  # Move to next phase
        current_direction, phase_duration = traffic_cycle[current_phase]  # Update new phase

    # Reset all lights to red
    for coords in dash_coordinates.values():
        for coord in coords:
            dash_colors[coord] = (255, 0, 0)

    # Set green and orange lights according to current phase
    if current_direction == "north":
        if elapsed_time < 27000:
            for coord in dash_coordinates["north"]:
                dash_colors[coord] = (0, 255, 0)  # North green
        elif 27000 <= elapsed_time < 29000:
            for coord in dash_coordinates["north"]:
                dash_colors[coord] = (255, 165, 0)  # North orange

    if current_phase > 0 and traffic_cycle[current_phase - 1][0] == "north" and elapsed_time >= 0:
        if elapsed_time < 12000:
            for coord in dash_coordinates["south"]:
                dash_colors[coord] = (0, 255, 0)  # South green
        elif 12000 <= elapsed_time < 14000:
            for coord in dash_coordinates["south"]:
                dash_colors[coord] = (255, 165, 0)  # South orange

    elif current_direction == "east":
        if elapsed_time < 27000:
            for coord in dash_coordinates["east"]:
                dash_colors[coord] = (0, 255, 0)  # East green
        elif 27000 <= elapsed_time < 29000:
            for coord in dash_coordinates["east"]:
                dash_colors[coord] = (255, 165, 0)  # East orange

    elif current_direction == "west":
        if elapsed_time < 12000:
            for coord in dash_coordinates["west"]:
                dash_colors[coord] = (0, 255, 0)  # West green
        elif 12000 <= elapsed_time < 14000:
            for coord in dash_coordinates["west"]:
                dash_colors[coord] = (255, 165, 0)  # West orange

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw traffic lights
    for (x, y), color in dash_colors.items():
        if (x, y) in dash_coordinates["east"] or (x, y) in dash_coordinates["west"]:  # Vertical dashes
            pygame.draw.line(screen, color, (x, y - 10), (x, y + 10), 5)
        else:  # Horizontal dashes
            pygame.draw.line(screen, color, (x - 10, y), (x + 10, y), 5)

    pygame.display.flip()

pygame.quit()
sys.exit()
