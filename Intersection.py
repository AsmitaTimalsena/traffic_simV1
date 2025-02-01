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
    ("south", 15000),  # After 15s of north, south also green for 15s
    ("east", 30000),   # East green for 30s
    ("west", 15000),   # West green for 15s (updated from 30s)
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

    # Set green lights according to current phase
    if current_direction == "north":
        for coord in dash_coordinates["north"]:
            dash_colors[coord] = (0, 255, 0)  # North green
        if elapsed_time >= 15000:  # After 15s, turn south green too
            for coord in dash_coordinates["south"]:
                dash_colors[coord] = (0, 255, 0)  # South green

    elif current_direction in dash_coordinates:  # East or West green
        for coord in dash_coordinates[current_direction]:
            dash_colors[coord] = (0, 255, 0)

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
