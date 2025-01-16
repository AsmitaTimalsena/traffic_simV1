import pygame 
import math

pygame.init()

# Screen dimensions
width, height = 1280, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Traffic Intersection Layout with 4-Lane Roads')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 0, 100)

# Lane properties
lane_width = 60
separator_thickness = 8
intersection_width = lane_width * 8
intersection_height = lane_width * 4

# Offset to shift the intersection downward
intersection_offset = 150

# Calculate the exact width for 4-lane roads
four_lane_width = lane_width * 4

# Added padding for south road (30 units on each side)
south_road_padding = 30

# Adjustment for alignment
overlap_correction = separator_thickness // 2

# Dashed line properties
dash_length = 20
gap_length = 20

def draw_dashed_line(surface, color, start_pos, end_pos, width=2):
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    angle = math.atan2(y2 - y1, x2 - x1)
    
    dx = (dash_length + gap_length) * math.cos(angle)
    dy = (dash_length + gap_length) * math.sin(angle)
    
    x, y = x1, y1
    segment_length = dash_length + gap_length
    num_segments = int(length / segment_length)
    
    for i in range(num_segments):
        dash_start = (x, y)
        dash_end = (x + dash_length * math.cos(angle),
                   y + dash_length * math.sin(angle))
        pygame.draw.line(surface, color, dash_start, dash_end, width)
        x += dx
        y += dy

try:
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLUE)

        # Calculate road center and intersection coordinates
        road_center_y = height // 2 + intersection_offset
        intersection_top = road_center_y - intersection_height // 2
        intersection_bottom = road_center_y + intersection_height // 2
        intersection_left = width // 2 - intersection_width // 2
        intersection_right = intersection_left + intersection_width

        # Calculate the starting x-coordinate for the south road with padding
        south_road_x = width // 2 - (four_lane_width // 2) - south_road_padding

        # Draw extended lanes
        # North lanes
        pygame.draw.rect(screen, GRAY, (width // 2 - 4 * lane_width, 0, lane_width * 8, intersection_top + overlap_correction))

        # South lanes
        pygame.draw.rect(screen, GRAY, (south_road_x, intersection_bottom - overlap_correction, four_lane_width + (south_road_padding * 2), height - intersection_bottom))

        # West lanes
        pygame.draw.rect(screen, GRAY, (0, road_center_y - 2 * lane_width, intersection_left + overlap_correction, four_lane_width))

        # East lanes
        pygame.draw.rect(screen, GRAY, (intersection_right - overlap_correction, road_center_y - 2 * lane_width, width - intersection_right + overlap_correction, four_lane_width))

        # Draw intersection
        pygame.draw.rect(screen, GRAY, (intersection_left - overlap_correction, intersection_top - overlap_correction, intersection_width + separator_thickness, intersection_height + separator_thickness))

        # Calculate consistent positions for all separators
        north_south_center = width // 2
        east_west_center = road_center_y

        # Draw solid middle separators
        # North road middle separator
        pygame.draw.line(screen, WHITE, (north_south_center, 0), (north_south_center, intersection_top), separator_thickness)
        
        # South road middle separator
        pygame.draw.line(screen, WHITE, (north_south_center, intersection_bottom), (north_south_center, height), separator_thickness)
        
        # West road middle separator
        pygame.draw.line(screen, WHITE, (0, east_west_center), (intersection_left, east_west_center), separator_thickness)
        
        # East road middle separator
        pygame.draw.line(screen, WHITE, (intersection_right, east_west_center), (width, east_west_center), separator_thickness)

        # Draw dashed lane separators with consistent positioning
        # South road dashed separators (shifted slightly inward)
        offset_adjustment = 10  # Amount to shift the dashed lines inward
        left_south_dash = north_south_center - (lane_width + lane_width // 2 - offset_adjustment)
        right_south_dash = north_south_center + (lane_width + lane_width // 2 - offset_adjustment)
        draw_dashed_line(screen, WHITE, (left_south_dash, intersection_bottom), (left_south_dash, height))
        draw_dashed_line(screen, WHITE, (right_south_dash, intersection_bottom), (right_south_dash, height))

        # West road dashed separators
        upper_west_dash = east_west_center - lane_width
        lower_west_dash = east_west_center + lane_width
        draw_dashed_line(screen, WHITE, (0, upper_west_dash), (intersection_left, upper_west_dash))
        draw_dashed_line(screen, WHITE, (0, lower_west_dash), (intersection_left, lower_west_dash))

        # East road dashed separators
        draw_dashed_line(screen, WHITE, (intersection_right, upper_west_dash), (width, upper_west_dash))
        draw_dashed_line(screen, WHITE, (intersection_right, lower_west_dash), (width, lower_west_dash))

                # North road dashed separators (adjusting distance between two dashed lines on each side)
        # Keep spacing consistent for dashed lines on the same side of the center
        outer_spacing = lane_width  # Distance for the outer dashed lines (unchanged)
        inner_spacing = lane_width + 85 # Slightly increased for more distance on the same side

        # Outer dashed lines (same as before)
        left_north_dash_1 = north_south_center - outer_spacing - lane_width // 2
        right_north_dash_1 = north_south_center + outer_spacing + lane_width // 2

        # Inner dashed lines (adjusted spacing between dashed lines on the same side)
        left_north_dash_2 = north_south_center - inner_spacing - lane_width // 2
        right_north_dash_2 = north_south_center + inner_spacing + lane_width // 2

        # Draw the dashed lines on each side of the north road
        draw_dashed_line(screen, WHITE, (left_north_dash_1, 0), (left_north_dash_1, intersection_top + dash_length))
        draw_dashed_line(screen, WHITE, (right_north_dash_1, 0), (right_north_dash_1, intersection_top + dash_length))
        
        draw_dashed_line(screen, WHITE, (left_north_dash_2, 0), (left_north_dash_2, intersection_top + dash_length))
        draw_dashed_line(screen, WHITE, (right_north_dash_2, 0), (right_north_dash_2, intersection_top + dash_length))

        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    pygame.quit()
    print("Program exited gracefully.")

pygame.quit()
