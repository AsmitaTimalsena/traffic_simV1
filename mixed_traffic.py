import pygame
import random

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shared lanes vehicle simulation')


WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Speed conversion, here we used logic(1 pixel = 5 meters, 60 FPS)
FPS = 60
METERS_PER_PIXEL = 5

# Vehicle settings
lanes = [45, 120, 180, 240]
SEPARATION_DISTANCE = 70
LANE_CHANGE_DISTANCE = 50 
OVERTAKE_DISTANCE = 50 

total_vehicles_passed = 0

font = pygame.font.Font(None, 24)

REAL_WORLD_HEIGHT = 200  # real world height in meters
SCREEN_HEIGHT = 700  

distance_per_pixel = REAL_WORLD_HEIGHT / SCREEN_HEIGHT  # 0.286 m/pixel

# Track vehicle speeds
bike_speed_data = {"display_speed": 0, "update_time": 0}
car_speed_data = {"display_speed": 0, "update_time": 0}

# Speed update interval (milliseconds)
SPEED_UPDATE_INTERVAL = 1000  # 1 second

start_time = pygame.time.get_ticks() 
class Vehicle:
   
    BIKE_SPEED_RANGE = (35, 42)  
    CAR_SPEED_RANGE = (30, 38) 

    def __init__(self, x, y, lane, vtype):
        self.x = x
        self.y = y
        self.lane = lane
        self.vtype = vtype

        if vtype == "bike":
            self.speed = random.randint(*self.BIKE_SPEED_RANGE)  # Random speed for bikes (in km/h)
        elif vtype == "car":
            self.speed = random.randint(*self.CAR_SPEED_RANGE)  # Random speed for cars (in km/h)

        #convert speed from km/h to pixels per frame
        self.speed = (self.speed * 1000) / (60 * 60 * METERS_PER_PIXEL)
        
        if vtype == "car":
            self.width = random.randint(15, 18)  
            self.height = random.randint(25, 28)  
        elif vtype == "bike":
            self.width = random.randint(10, 12)  
            self.height = random.randint(20, 25)  
        
        self.target_lane = self.lane
        self.lane_change_progress = 0  
        self.change_direction_progress = 0  # How far the vehicle has moved to its target lane
        self.lane_change_speed_factor = 0.5  # factor to reduce speed during lane change
        self.original_speed = self.speed  

    def draw(self, screen):
        if self.vtype == "car":
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        elif self.vtype == "bike":
            pygame.draw.ellipse(screen, YELLOW, (self.x, self.y, self.width, self.height))

    def move(self):
        global total_vehicles_passed
        if self.lane_change_progress < 1: #reduce speed during lane change
            self.speed = self.original_speed * self.lane_change_speed_factor

            self.y += self.speed
            if abs(self.x - self.target_lane) > 1: #if chainging lane
               
                self.x += (self.target_lane - self.x) * 0.1
            else:
                self.x = self.target_lane
                self.lane = self.target_lane
                self.lane_change_progress = 1
                # original speed after lane change
                self.speed = self.original_speed
        else:
            self.y += self.speed

    def adjust_speed(self, vehicles):
       
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
    vtype = random.choices(["bike", "car"], weights=[70, 30])[0]  # 65% for bike, 35% for car
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

    pygame.draw.line(screen, WHITE, (300, 0), (300, height), 5)
    pygame.draw.line(screen, WHITE, (310, 0), (310, height), 5)

    bike_speeds = []
    car_speeds = []
    for vehicle in vehicles:
        vehicle.adjust_speed(vehicles)  # Adjust speed based on proximity
        vehicle.attempt_lane_change(vehicles)  # Try to change lane if necessary
        vehicle.move()  # Move the vehicle
        if vehicle.y > height:
            vehicle.y = random.randint(-height, 0)  # Respawn at the top
            total_vehicles_passed += 1  # Increase the counter when the vehicle passes the screen
        vehicle.draw(screen)

        # Collect speed data
        if vehicle.vtype == "bike":
            bike_speeds.append(vehicle.speed * (60 * 60 * METERS_PER_PIXEL) / 1000)  # Convert back to km/h
        elif vehicle.vtype == "car":
            car_speeds.append(vehicle.speed * (60 * 60 * METERS_PER_PIXEL) / 1000)  # Convert back to km/h


    current_time = pygame.time.get_ticks()
    if current_time - bike_speed_data["update_time"] >= SPEED_UPDATE_INTERVAL:
        if bike_speeds:
            bike_speed_data["display_speed"] = sum(bike_speeds) / len(bike_speeds)
            print(f"[Time: {elapsed_minutes:02}:{elapsed_seconds:02}] Bike Avg Speed: {bike_speed_data['display_speed']:.2f} km/hr") 
        bike_speed_data["update_time"] = current_time

    if current_time - car_speed_data["update_time"] >= SPEED_UPDATE_INTERVAL:
        if car_speeds:
            car_speed_data["display_speed"] = sum(car_speeds) / len(car_speeds)
            print(f"[Time: {elapsed_minutes:02}:{elapsed_seconds:02}] Car Avg Speed: {car_speed_data['display_speed']:.2f} km/hr")
        car_speed_data["update_time"] = current_time

    #  elapsed time calculation
    elapsed_time = pygame.time.get_ticks() - start_time  # in milliseconds
    elapsed_seconds = elapsed_time // 1000  #  seconds
    elapsed_minutes = elapsed_seconds // 60  #  minutes
    elapsed_seconds %= 60  # remaining seconds
   

    # Display the metrics
    font = pygame.font.Font(None, 24)
    y_offset = 150
    text = font.render(f"Total Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (400, y_offset))
    timer_text = font.render(f"Time: {elapsed_minutes:02}:{elapsed_seconds:02}", True, WHITE)
    screen.blit(timer_text, (400, y_offset + 100))
   
    y_offset += 30
    text = font.render(f"Bike Avg Speed: {bike_speed_data['display_speed']:.2f} km/hr", True, WHITE)
    screen.blit(text, (400, y_offset))
    y_offset += 30
    text = font.render(f"Car Avg Speed: {car_speed_data['display_speed']:.2f} km/hr", True, WHITE)
    screen.blit(text, (400, y_offset))

    pygame.display.flip()
    clock.tick(FPS) 
pygame.quit()