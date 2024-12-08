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
        self.x = lane_position  # Initial lane position
        self.y = random.randint(-height, -50)  # Start above the screen
        self.speed = random.uniform(1, 2) if vehicle_type == "motorcycle" else random.uniform(0.5, 1.5)
        self.original_speed = self.speed
        self.max_speed = self.speed * 1.5
        self.width = 10 if vehicle_type == "motorcycle" else random.randint(13, 20)
        self.length = 20 if vehicle_type == "motorcycle" else random.randint(23, 33)
        self.target_x = self.x  # Target lane for smooth transitions
        self.transitioning = False
        self.last_lane_change_time = 0  # Cooldown timer for lane changes

    def fall(self, vehicles_in_lane, left_lane_vehicles, right_lane_vehicles, safe_threshold):
        current_time = pygame.time.get_ticks()

        # Increase speed over time to simulate acceleration
        self.speed = min(self.speed + 0.02, self.max_speed)

        # Collision avoidance logic for vehicles ahead
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:  # Vehicle ahead
                distance = other_vehicle.y - self.y
                if distance < safe_threshold:
                    # Stop or slow down if too close to the vehicle ahead
                    self.speed = max(self.speed - 0.1, 0)
                    break
                else:
                    # If there's enough space, allow normal speed or speeding up
                    self.speed = min(self.speed + 0.02, self.max_speed)

        # Aggressive Lane Change: Change lane when opportunity arises
        if self.vehicle_type == "motorcycle" and not self.transitioning:
            if any(v.y - self.y < 50 for v in vehicles_in_lane if v != self) and current_time - self.last_lane_change_time > 1000:  # 1-second cooldown
                # Check if there's a vehicle ahead in the current lane (within the safe threshold)
                vehicle_ahead_in_lane = any(v.y - self.y < safe_threshold for v in vehicles_in_lane if v != self)

                if vehicle_ahead_in_lane:
                    # Check if adjacent lanes have enough space
                    if self.x == 45 and left_lane_vehicles is not None:  # from lane 45 to 120
                        can_switch_left = all(abs(v.y - self.y) >= 100 for v in left_lane_vehicles)
                        if can_switch_left:
                            self.target_x = 120  # Move to the left lane (lane 120)
                            self.transitioning = True
                            self.last_lane_change_time = current_time
                    elif self.x == 120 and left_lane_vehicles is not None:  # from lane 120 to 45
                        can_switch_left = all(abs(v.y - self.y) >= 100 for v in left_lane_vehicles)
                        if can_switch_left:
                            self.target_x = 45  # Move to the left lane (lane 45)
                            self.transitioning = True
                            self.last_lane_change_time = current_time
                    elif self.x == 120 and right_lane_vehicles is not None:  # from lane 120 to 180
                        can_switch_right = all(abs(v.y - self.y) >= 100 for v in right_lane_vehicles)
                        if can_switch_right:
                            self.target_x = 180  # Move to the right lane (lane 180)
                            self.transitioning = True
                            self.last_lane_change_time = current_time
                    elif self.x == 180 and right_lane_vehicles is not None:  # from lane 180 to 240
                        can_switch_right = all(abs(v.y - self.y) >= 100 for v in right_lane_vehicles)
                        if can_switch_right:
                            self.target_x = 240  # Move to the right lane (lane 240)
                            self.transitioning = True
                            self.last_lane_change_time = current_time
                    elif self.x == 240 and left_lane_vehicles is not None:  # from lane 240 to 180
                        can_switch_left = all(abs(v.y - self.y) >= 100 for v in left_lane_vehicles)
                        if can_switch_left:
                            self.target_x = 180  # Move to the left lane (lane 180)
                            self.transitioning = True
                            self.last_lane_change_time = current_time

        # Smoothly transition to the target lane
        if self.x != self.target_x:
            if abs(self.x - self.target_x) < 1:
                self.x = self.target_x
                self.transitioning = False
            elif self.x < self.target_x:
                self.x += 1
            elif self.x > self.target_x:
                self.x -= 1

        # Move forward
        self.y += self.speed

        # Reset if off-screen
        if self.y > height:
            self.y = random.randint(-height, -50)
            self.transitioning = False  # Reset transition state

    def draw(self, surface):
        if self.vehicle_type == "motorcycle":
            pygame.draw.ellipse(surface, YELLOW, (self.x - self.width // 2, int(self.y), self.width, self.length))
        elif self.vehicle_type == "car":
            pygame.draw.rect(surface, WHITE, (self.x - self.width // 2, int(self.y), self.width, self.length))


# Lane positions
lane_positions = [45, 120, 180, 240]
vehicles = {pos: [] for pos in lane_positions}  # Store vehicles by lane
safe_threshold = 50  # Safe distance

# Timers for vehicle generation
timers = {pos: pygame.USEREVENT + i for i, pos in enumerate(lane_positions)}
for timer in timers.values():
    pygame.time.set_timer(timer, 2000)  # New vehicle every 2 seconds

# Function to check if there is enough space to spawn a vehicle
def is_safe_to_spawn(lane, vehicles_in_lane):
    for other_vehicle in vehicles_in_lane:
        if abs(other_vehicle.y - 0) < safe_threshold:  # Check if there's not enough space at the top of the screen
            return False
    return True

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Generate new vehicles only if there's enough space
        for lane, timer in timers.items():
            if event.type == timer:
                vehicle_type = random.choices(["motorcycle", "car"], [0.7, 0.3])[0]
                # Check if there is enough space to spawn a new vehicle
                if is_safe_to_spawn(lane, vehicles[lane]):
                    vehicles[lane].append(Vehicle(vehicle_type, lane))

    screen.fill(BLUE)

    # Draw lane markings
    for y in range(0, height, 20):
        pygame.draw.line(screen, WHITE, (150, y), (150, y + 10), 2)

    # Update and draw vehicles
    for lane in lane_positions:
        left_lane_vehicles = vehicles.get(lane - 75) if lane > min(lane_positions) else None
        right_lane_vehicles = vehicles.get(lane + 75) if lane < max(lane_positions) else None

        for vehicle in vehicles[lane][:]:
            vehicle.fall(vehicles[lane], left_lane_vehicles, right_lane_vehicles, safe_threshold)
            vehicle.draw(screen)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
