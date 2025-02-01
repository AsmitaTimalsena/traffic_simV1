import pygame
import random

pygame.init()

width, height = 300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shared lanes vehicle simulation')

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Speed conversion (1 pixel = 5 meters, 60 FPS)
FPS = 60
METERS_PER_PIXEL = 5  # Adjusted scale

# Vehicle settings
lanes = [45, 120, 180, 240]
SEPARATION_DISTANCE = 70
LANE_CHANGE_DISTANCE = 50  # Reduced distance to make lane changes more frequent
OVERTAKE_DISTANCE = 50  # How close a vehicle needs to be to start slowing down

# Initialize total vehicles passed counter
total_vehicles_passed = 0

# Font for rendering the text
font = pygame.font.Font(None, 24)

class Vehicle:
    # Class-level constants for speed ranges
    BIKE_SPEED_RANGE = (35, 40)  # km/h
    CAR_SPEED_RANGE = (30, 35)   # km/h

    def __init__(self, x, y, lane, vtype):
        self.x = x
        self.y = y
        self.lane = lane
        self.vtype = vtype

        # Randomize speed within a specific range for each vehicle type
        if vtype == "bike":
            self.speed = random.randint(*self.BIKE_SPEED_RANGE)  # Random speed for bikes (in km/h)
        elif vtype == "car":
            self.speed = random.randint(*self.CAR_SPEED_RANGE)  # Random speed for cars (in km/h)

        # Convert speed from km/h to pixels per frame
        self.speed = (self.speed * 1000) / (60 * 60 * METERS_PER_PIXEL)
        
        # Randomize vehicle size
        if vtype == "car":
            self.width = random.randint(15, 18)  # Random width for cars
            self.height = random.randint(25, 28)  # Random height for cars
        elif vtype == "bike":
            self.width = random.randint(10, 12)  # Random width for bikes
            self.height = random.randint(20, 25)  # Random height for bikes
        
        self.target_lane = self.lane
        self.lane_change_progress = 0  # 0 means not yet in the target lane
        self.change_direction_progress = 0  # How far the vehicle has moved to its target lane
        self.lane_change_speed_factor = 0.5  # Factor to reduce speed during lane change
        self.original_speed = self.speed  # Store the original speed

    def draw(self, screen):
        if self.vtype == "car":
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        elif self.vtype == "bike":
            pygame.draw.ellipse(screen, YELLOW, (self.x, self.y, self.width, self.height))

    def move(self):
        global total_vehicles_passed
        if self.lane_change_progress < 1:
            # Reduce speed during lane change
            self.speed = self.original_speed * self.lane_change_speed_factor
            # Smoothly move to the target lane along y-axis, and then adjust the x-coordinate
            self.y += self.speed
            if abs(self.x - self.target_lane) > 1:
                # Adjust the x-coordinate to the target lane gradually
                self.x += (self.target_lane - self.x) * 0.1
            else:
                self.x = self.target_lane
                self.lane = self.target_lane
                self.lane_change_progress = 1
                # Restore original speed after lane change is complete
                self.speed = self.original_speed
        else:
            self.y += self.speed

    def adjust_speed(self, vehicles):
        # Adjust speed if another vehicle is too close
        for other in vehicles:
            if other != self and other.lane == self.lane:
                distance = other.y - self.y
                if 0 < distance < OVERTAKE_DISTANCE:
                    # Slow down if too close
                    self.speed = max(self.speed - 0.05, self.get_base_speed() * 0.5)
                    return
        # Reset speed if no vehicle is too close
        if self.speed < self.get_base_speed():
            self.speed += 0.05  # Gradually return to normal speed

    def get_base_speed(self):
        # Get the base speed for the vehicle type
        if self.vtype == "bike":
            return (self.BIKE_SPEED_RANGE[0] * 1000) / (60 * 60 * METERS_PER_PIXEL)
        elif self.vtype == "car":
            return (self.CAR_SPEED_RANGE[0] * 1000) / (60 * 60 * METERS_PER_PIXEL)

    def attempt_lane_change(self, vehicles):
        if self.vtype != "bike":
            return  # Only bikes change lanes

        for other in vehicles:
            if other != self and other.lane == self.lane:
                distance = other.y - self.y
                if 0 < distance < LANE_CHANGE_DISTANCE and self.speed > other.speed:
                    # Check if the bike should change lanes to overtake
                    left_lane = self.lane - 75
                    if left_lane >= 45 and self.can_change_lane(vehicles, left_lane):
                        self.target_lane = left_lane
                        self.lane_change_progress = 0
                        self.change_direction_progress = 0
                        return

                    # Check right lane
                    right_lane = self.lane + 75
                    if right_lane <= 240 and self.can_change_lane(vehicles, right_lane):
                        self.target_lane = right_lane
                        self.lane_change_progress = 0
                        self.change_direction_progress = 0
                        return

    def can_change_lane(self, vehicles, target_lane):
        for other in vehicles:
            if other.lane == target_lane:
                distance = abs(other.y - self.y)
                if distance < LANE_CHANGE_DISTANCE:
                    return False  # No space in target lane
        return True

# Initialize vehicles
vehicles = []
for i in range(20):  # Increased number of vehicles from 10 to 20
    lane = random.choice(lanes)  # Select randomly from valid lanes [45, 120, 180, 240]
    vtype = random.choices(["bike", "car"], weights=[65, 35])[0]  # 65% for bike, 35% for car
    x = lane
    y = random.randint(-height, 0)  # Random y-coordinate (off-screen to start)
    vehicles.append(Vehicle(x, y, lane, vtype))

# Main game loop
running = True
clock = pygame.time.Clock()  # Control the frame rate
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the blue color
    screen.fill(BLUE)

    # Draw a white dashed vertical line starting from (200, 0) downwards
    dash_length = 20
    gap_length = 10
    start_x = 150
    start_y = 0

    for y in range(start_y, height, dash_length + gap_length):
        pygame.draw.line(screen, WHITE, (start_x, y), (start_x, y + dash_length), 2)

    # Update and draw vehicles
    for vehicle in vehicles:
        vehicle.adjust_speed(vehicles)  # Adjust speed based on proximity
        vehicle.attempt_lane_change(vehicles)  # Try to change lane if necessary
        vehicle.move()  # Move the vehicle
        if vehicle.y > height:
            vehicle.y = random.randint(-height, 0)  # Respawn at the top
            total_vehicles_passed += 1  # Increase the counter when the vehicle passes the screen
        vehicle.draw(screen)

    font = pygame.font.Font(None, 28)
    text = font.render(f"Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)  # Maintain 60 FPS

pygame.quit()