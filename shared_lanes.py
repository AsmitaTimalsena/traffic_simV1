import pygame
import random

pygame.init()
# Screen dimensions
width, height = 300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shared lanes vehicle simulation')

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)

class Vehicle:
    def __init__(self, vehicle_type, lane_position):
        self.vehicle_type = vehicle_type
        self.x = lane_position  # Assigned specific lane position
        self.y = random.randint(-height, 0)  # Start above the screen
        self.speed = random.uniform(1, 2) if vehicle_type == "motorcycle" else random.uniform(0.5, 1.5)
        self.original_speed = self.speed  # Keep track of the original speed
        self.max_speed = self.speed * 1.5  # Vehicles can increase speed up to 1.5x original

        # Define size
        if vehicle_type == "motorcycle":
            self.size = random.randint(8, 10)  # Diameter of the motorcycle (circle)
            self.width = self.size * 2  # Width of the motorcycle for lane check
        elif vehicle_type == "car":
            self.width = random.randint(13, 20)  # Width of the car
            self.length = random.randint(23, 33)  # Length of the car

        self.target_x = self.x  # target_x to smoothly transition lanes
        self.transitioning = False  # Flag to ensure only one lane change at a time

    def fall(self, vehicles_in_lane, adjacent_lane_vehicles, safe_threshold, ample_space):
        global vehicle_passed_count

        # Default to max speed
        self.speed = min(self.speed + 0.02, self.max_speed)

        # Adjust speed or stop based on distance to the preceding vehicle
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:  # Check vehicles ahead
                distance = other_vehicle.y - self.y
                if distance < safe_threshold:  # Too close
                    self.speed = 0  # Stop moving temporarily

                    # Attempt to change lanes if motorcycle
                    if self.vehicle_type == "motorcycle" and not self.transitioning:
                        if adjacent_lane_vehicles is not None:
                            can_switch_lane = True
                            for adj_vehicle in adjacent_lane_vehicles:
                                if abs(adj_vehicle.y - self.y) < ample_space:
                                    can_switch_lane = False
                                    break
                            if can_switch_lane:
                                self.target_x = adjacent_lane_vehicles[0].x if adjacent_lane_vehicles else self.x
                                self.transitioning = True
                                break
                    break

        # Attempt more frequent lane changes for motorcycles
        if self.vehicle_type == "motorcycle" and not self.transitioning:
            if adjacent_lane_vehicles is not None:
                can_switch_lane = True
                for adj_vehicle in adjacent_lane_vehicles:
                    if abs(adj_vehicle.y - self.y) < ample_space:
                        can_switch_lane = False
                        break
                if can_switch_lane:
                    self.target_x = adjacent_lane_vehicles[0].x if adjacent_lane_vehicles else self.x
                    self.transitioning = True

        # Smoothly move towards the target_x position
        if self.x < self.target_x:
            self.x += 0.5  # Move to the right smoothly
        elif self.x > self.target_x:
            self.x -= 0.5  # Move to the left smoothly

        # Update position
        self.y += self.speed

        # Reset if it goes off-screen
        if self.y > height:
            self.y = random.randint(-height, 0)
            vehicle_passed_count += 1  # Increment vehicle passed count
            self.transitioning = False  # Reset transition state when the vehicle resets

    def draw(self, surface):
        if self.vehicle_type == "motorcycle":
            # Draw an oval instead of a circle
            oval_width = self.size * 2  # Make the oval slightly wider than the size
            oval_height = self.size     # Use the size as the height
            pygame.draw.ellipse(surface, YELLOW, (self.x - oval_height // 2, int(self.y) - oval_width // 2, oval_height, oval_width))
        elif self.vehicle_type == "car":
            pygame.draw.rect(surface, WHITE, (self.x, int(self.y), self.width, self.length))

# Predefined lane positions
lane_positions = [45, 120, 180, 240]

# Define probabilities for vehicle types
vehicle_types = ["motorcycle", "car"]
probabilities = [0.63, 0.35]  # 65% for motorcycles, 35% for cars

# Create a dictionary to store vehicles for each lane
vehicles = {pos: [] for pos in lane_positions}  # Separate list for each lane position

# Safe distance threshold
safe_threshold = 70
ample_space = 120

# Timers for each lane position
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(lane_positions)}

# Set 3-second timers for each lane position
for timer in timers.values():
    pygame.time.set_timer(timer, 3000)

# Vehicle passed count
vehicle_passed_count = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Generate vehicles for each lane position independently
        for pos, timer in timers.items():
            if event.type == timer:
                vehicle_type = random.choices(vehicle_types, probabilities)[0]
                new_vehicle = Vehicle(vehicle_type, pos)
                vehicles[pos].append(new_vehicle)

    screen.fill(BLUE)

    for y in range(0, height, 20):  # Adjust the step to control the gap size
        pygame.draw.line(screen, WHITE, (150, y), (150, y + 10), 2) 

    # Update and draw vehicles
    for lane in lane_positions:
        adjacent_lane_vehicles = None
        if lane == 45:
            adjacent_lane_vehicles = vehicles[120]
        elif lane == 120:
            adjacent_lane_vehicles = vehicles[45] + vehicles[180]
        elif lane == 180:
            adjacent_lane_vehicles = vehicles[120] + vehicles[240]
        elif lane == 240:
            adjacent_lane_vehicles = vehicles[180]

        for vehicle in vehicles[lane][:]:  # Use a copy of the list to avoid modification issues
            vehicle.fall(vehicles[lane], adjacent_lane_vehicles, safe_threshold, ample_space)  # Ensure safe distance and switching
            vehicle.draw(screen)

    # Display vehicle passed count
    font = pygame.font.Font(None, 26)
    passed_text = font.render(f'Vehicles Passed: {vehicle_passed_count}', True, WHITE)
    screen.blit(passed_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
