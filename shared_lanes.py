import pygame
import random

pygame.init()
# Screen dimensions
width, height = 400, 700
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
            self.width = self.size * 2  # width of the motorcycle for lane check
        elif vehicle_type == "car":
            self.width = random.randint(13, 20)  # Width of the car
            self.length = random.randint(23, 33)  # Length of the car


        self.target_x = self.x  # target_x to smoothly transition lanes
        self.transitioning = False  # Flag to ensure only one lane change at a time
        self.last_lane_change_time = 0  # Track the time since the last lane change


    def fall(self, vehicles_in_lane, left_lane_vehicles, right_lane_vehicles, safe_threshold):
        # Default to max speed
        self.speed = min(self.speed + 0.02, self.max_speed)


        # Adjust speed or stop based on distance to the preceding vehicle
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:  # Check vehicles ahead
                distance = other_vehicle.y - self.y
                if distance < safe_threshold:  # Too close
                    self.speed = 0  # Stop moving temporarily
                    break
                else:
                    # If no vehicle is in front, accelerate up to max speed
                    self.speed = min(self.speed + 0.01, self.max_speed)


        # Attempt to change lanes if there is enough space
        if self.vehicle_type == "motorcycle" and not self.transitioning:
            # Lane change logic based on vehicle type and current lane


            if self.x == 60 and self.y < height and (len(vehicles_in_lane) > 0 and (vehicles_in_lane[0].y - self.y) < safe_threshold):
                # Check if there's enough space in the adjacent lane 120
                if right_lane_vehicles is not None:
                    can_switch_right = True
                    for other_vehicle in right_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < safe_threshold:  # Check vertical space in the right lane
                            can_switch_right = False
                            break
                    if can_switch_right:
                        self.target_x = 120  # Move to 120
                        self.transitioning = True  # Mark as transitioning


            elif self.x == 120 and self.y < height and (len(vehicles_in_lane) > 0 and (vehicles_in_lane[0].y - self.y) < safe_threshold):
                # Check if there's enough space in the adjacent lane 60 or 260
                if left_lane_vehicles is not None:
                    can_switch_left = True
                    for other_vehicle in left_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < safe_threshold:  # Check vertical space in the left lane
                            can_switch_left = False
                            break
                    if can_switch_left:
                        self.target_x = 60  # Move to 60
                        self.transitioning = True  # Mark as transitioning


                if right_lane_vehicles is not None:
                    can_switch_right = True
                    for other_vehicle in right_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < safe_threshold:  # Check vertical space in the right lane
                            can_switch_right = False
                            break
                    if can_switch_right:
                        self.target_x = 260  # Move to 260
                        self.transitioning = True  # Mark as transitioning


            elif self.x == 260 and self.y < height and (len(vehicles_in_lane) > 0 and (vehicles_in_lane[0].y - self.y) < safe_threshold):
                # Check if there's enough space in the adjacent lane 330 or 120
                if right_lane_vehicles is not None:
                    can_switch_right = True
                    for other_vehicle in right_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < safe_threshold:  
                            can_switch_right = False
                            break
                    if can_switch_right:
                        self.target_x = 330  # Move to 330
                        self.transitioning = True  # Mark as transitioning


                if left_lane_vehicles is not None:
                    can_switch_left = True
                    for other_vehicle in left_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < safe_threshold:  # Check vertical space in the left lane
                            can_switch_left = False
                            break
                    if can_switch_left:
                        self.target_x = 120  # Move to 120
                        self.transitioning = True  # Mark as transitioning


            elif self.x == 330 and self.y < height and (len(vehicles_in_lane) > 0 and (vehicles_in_lane[0].y - self.y) < safe_threshold):
                # Check if there's enough space in the adjacent lane 260
                if left_lane_vehicles is not None:
                    can_switch_left = True
                    for other_vehicle in left_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < safe_threshold:  # Check vertical space in the left lane
                            can_switch_left = False
                            break
                    if can_switch_left:
                        self.target_x = 260  # Move to 260
                        self.transitioning = True  # Mark as transitioning


        # After lane change, check the new lane for collisions with vehicles ahead and behind
        if self.x != self.target_x:
            # Check for vehicles ahead and behind in the new lane
            new_lane_vehicles = left_lane_vehicles if self.target_x in left_lane_positions else right_lane_vehicles


            # Collision avoidance after lane change
            if new_lane_vehicles is not None:
                # Check vehicles in the target lane for collision
                for other_vehicle in new_lane_vehicles:
                    if other_vehicle != self:
                        if abs(other_vehicle.y - self.y) < safe_threshold:
                            # Adjust speed if there's a potential collision
                            self.speed = 0  # Stop temporarily
                            break

                        
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
left_lane_positions = [60, 120]
right_lane_positions = [260, 330]
lane_positions = left_lane_positions + right_lane_positions


# Define probabilities for vehicle types
vehicle_types = ["motorcycle", "car"]
probabilities = [0.6, 0.4]  # 60% for motorcycles, 40% for cars


# Create a dictionary to store vehicles for each lane
vehicles = {pos: [] for pos in lane_positions}  # Separate list for each lane position

# Safe distance threshold
safe_threshold = 50
# Timers for each lane position
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(lane_positions)}


# Set 3-second timers for each lane position
for timer in timers.values():
    pygame.time.set_timer(timer, 3000)


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

        pygame.draw.line(screen, WHITE, (200, y), (200, y + 10), 2) 
    # Update and draw vehicles
    for lane in lane_positions:
        # Check if there’s a valid adjacent lane for lane-switching
        right_lane_vehicles = vehicles.get(lane + 200) if lane in left_lane_positions else None
        left_lane_vehicles = vehicles.get(lane - 200) if lane in right_lane_positions else None

        # Iterate over vehicles, updating their behavior
        for vehicle in vehicles[lane][:]:  # Use a copy of the list to avoid modification issues
            vehicle.fall(vehicles[lane], left_lane_vehicles, right_lane_vehicles, safe_threshold)  # Ensure safe distance and switching
            vehicle.draw(screen)

    pygame.display.flip()
    pygame.time.delay(30)
pygame.quit()






