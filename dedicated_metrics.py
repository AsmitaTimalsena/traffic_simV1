import pygame
import random
import time

pygame.init()

width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dedicated lanes vehicle simulation')

REAL_WORLD_HEIGHT = 200  
SCREEN_HEIGHT = 700  
FPS = 30  
distance_per_pixel = REAL_WORLD_HEIGHT / SCREEN_HEIGHT  # 0.286 m/pixel

MOTORCYCLE_MIN_SPEED = 6
MOTORCYCLE_MAX_SPEED = 7
CAR_MIN_SPEED = 4
CAR_MAX_SPEED = 5.5

WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)  # Added for collision indication

total_vehicles_passed = 0
collision_count = 0  # Initialize collision counter

car_velocity_data = {
    45: {"display_speed": 0, "update_time": 0},
    240: {"display_speed": 0, "update_time": 0}
}

motorcycle_velocity_data = {
    120: {"display_speed": 0, "update_time": 0},
    180: {"display_speed": 0, "update_time": 0}
}

SPEED_UPDATE_INTERVAL = 1000  

def calculate_real_speed(pixels_per_frame):
    """Convert simulation speed to km/h"""
    meters_per_frame = pixels_per_frame * distance_per_pixel
    meters_per_second = meters_per_frame * FPS
    kilometers_per_hour = (meters_per_second * 3600) / 1000
    return kilometers_per_hour

def normalize_speed(speed, vehicle_type):
    """Normalize speed to the appropriate range"""
    if vehicle_type == "motorcycle":
        return max(MOTORCYCLE_MIN_SPEED, min(MOTORCYCLE_MAX_SPEED, speed))
    else:
        return max(CAR_MIN_SPEED, min(CAR_MAX_SPEED, speed))

start_time = pygame.time.get_ticks()

class Vehicle:
    def __init__(self, vehicle_type, lane_position):
        self.vehicle_type = vehicle_type
        self.x = lane_position 
        self.y = random.randint(-height, -50)  # Start vehicles off screen but not at the very edge
        self.in_collision = False  # Track if vehicle is currently in collision
        self.has_collided_with = set()  # Set of vehicles this one has already collided with
        self.on_screen = False  # Track if vehicle is on screen

        if vehicle_type == "motorcycle":
            self.max_speed = random.uniform(MOTORCYCLE_MIN_SPEED, MOTORCYCLE_MAX_SPEED)
            self.speed = self.max_speed
        else:
            self.max_speed = random.uniform(CAR_MIN_SPEED, CAR_MAX_SPEED)
            self.speed = self.max_speed
            
        self.original_speed = self.speed
        self.prev_y = self.y

        if vehicle_type == "motorcycle":
            self.size = random.randint(8, 10)  
            self.width = self.size
            self.length = self.size * 2
        elif vehicle_type == "car":
            self.width = random.randint(13, 20)  
            self.length = random.randint(23, 33) 

    def fall(self, vehicles_in_lane, safe_threshold):
        global total_vehicles_passed
        self.prev_y = self.y

        closest_vehicle = None
        closest_distance = float('inf')

        # Find the closest vehicle ahead in the same lane
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:
                distance = other_vehicle.y - self.y
                if distance < closest_distance:
                    closest_distance = distance
                    closest_vehicle = other_vehicle

        # Adjust speed based on proximity to the closest vehicle
        if closest_vehicle:
            if closest_distance < safe_threshold:
                # Too close, adjust speed to avoid collision
                self.speed = max(closest_vehicle.speed - 0.5, 0)
            elif closest_distance > 70:
                self.speed = min(self.max_speed, self.original_speed + 0.5)
            else:
                # Moderate distance, maintain original speed
                self.speed = self.original_speed
        else:
            # No vehicle ahead, move at maximum speed
            self.speed = self.max_speed

        # Scale the movement speed while keeping the display speed in range
        movement_scale = 1 
        self.y += self.speed * movement_scale
        
        # Check if vehicle entered screen
        if not self.on_screen and self.y > 0:
            self.on_screen = True
            
        # Check if vehicle exited screen
        if self.y > height:
            self.y = random.randint(-height, -50)  # Start further off screen
            self.prev_y = self.y
            self.on_screen = False
            self.has_collided_with.clear()  # Reset collision history
            self.in_collision = False
            total_vehicles_passed += 1

    def get_current_speed(self):
        """Get the normalized speed for the vehicle type"""
        return normalize_speed(self.speed, self.vehicle_type)

    def draw(self, surface):
        if self.vehicle_type == "motorcycle":
            # Use red color for collisions, yellow for normal
            color = RED if self.in_collision else YELLOW
            oval_width = self.size * 2  
            oval_height = self.size     
            pygame.draw.ellipse(surface, color, (self.x - oval_height // 2, int(self.y) - oval_width // 2, oval_height, oval_width))
        elif self.vehicle_type == "car":
            # Use red color for collisions, white for normal
            color = RED if self.in_collision else WHITE
            pygame.draw.rect(surface, color, (self.x, int(self.y), self.width, self.length))

    def get_rect(self):
        # Return a pygame Rect for collision detection
        if self.vehicle_type == "motorcycle":
            oval_width = self.size * 2
            oval_height = self.size
            return pygame.Rect(self.x - oval_height // 2, int(self.y) - oval_width // 2, oval_height, oval_width)
        else:  # car
            return pygame.Rect(self.x, int(self.y), self.width, self.length)

def check_collisions():
    # For dedicated lanes, we should check collisions only within the same lane
    # Since vehicles stay in their own lanes, we should only detect rear-end collisions
    global collision_count
    
    for lane, lane_vehicles in vehicles.items():
        # Sort vehicles in lane by y-position (front to back)
        sorted_vehicles = sorted(lane_vehicles, key=lambda v: v.y)
        
        # Check for collisions between consecutive vehicles
        for i in range(len(sorted_vehicles) - 1):
            front_vehicle = sorted_vehicles[i]
            back_vehicle = sorted_vehicles[i + 1]
            
            # Skip if either vehicle is not on screen
            if not front_vehicle.on_screen or not back_vehicle.on_screen:
                continue
                
            # Skip if vehicles are far apart
            if back_vehicle.y + back_vehicle.length < front_vehicle.y:
                continue
                
            # Create Rect objects for collision detection
            rect1 = front_vehicle.get_rect()
            rect2 = back_vehicle.get_rect()
            
            # Check for collision
            if rect1.colliderect(rect2):
                # Mark both vehicles as in collision for visual effect
                front_vehicle.in_collision = True
                back_vehicle.in_collision = True
                
                # Only count collision if these two vehicles haven't collided before
                if back_vehicle not in front_vehicle.has_collided_with:
                    front_vehicle.has_collided_with.add(back_vehicle)
                    back_vehicle.has_collided_with.add(front_vehicle)
                    collision_count += 1
                    print(f"Collision detected: {front_vehicle.vehicle_type}-{back_vehicle.vehicle_type} in lane {lane}")
            else:
                # Reset collision state if vehicles are no longer colliding
                if front_vehicle.in_collision and back_vehicle.in_collision:
                    front_vehicle.in_collision = False
                    back_vehicle.in_collision = False

motorcycle_positions = [120, 180]
car_positions = [45, 240]
vehicle_types = ["motorcycle", "car"]
probabilities = [0.7, 0.3]  

vehicles = {pos: [] for pos in motorcycle_positions + car_positions}
safe_threshold = 50

# Timers for each lane position
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(motorcycle_positions + car_positions)}

# Reduce vehicle generation frequency to avoid overcrowding
for pos in motorcycle_positions:
    pygame.time.set_timer(timers[pos], 2000)  # Every 2 seconds for motorcycles
    
for pos in car_positions:
    pygame.time.set_timer(timers[pos], 3000)  # Every 3 seconds for cars

# Spawn initial vehicles immediately
for pos in motorcycle_positions:
    new_vehicle = Vehicle("motorcycle", pos)
    vehicles[pos].append(new_vehicle)

for pos in car_positions:
    new_vehicle = Vehicle("car", pos)
    vehicles[pos].append(new_vehicle)

last_print_time = time.time()
def calculate_average_speeds():
    car_speeds = []
    for lane in car_positions:
        if car_velocity_data[lane]['display_speed'] > 0:
            car_speeds.append(car_velocity_data[lane]['display_speed'] * scaling_factor)
    car_avg = sum(car_speeds) / len(car_speeds) if car_speeds else 0

    bike_speeds = []
    for lane in motorcycle_positions:
        if motorcycle_velocity_data[lane]['display_speed'] > 0:
            bike_speeds.append(motorcycle_velocity_data[lane]['display_speed'] * scaling_factor)
    bike_avg = sum(bike_speeds) / len(bike_speeds) if bike_speeds else 0

    return car_avg, bike_avg

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        for pos, timer in timers.items():
            if event.type == timer:
                if pos in motorcycle_positions:
                    # Ensure sufficient spacing between motorcycles
                    if not vehicles[pos] or vehicles[pos][-1].y > 100:  # Increased gap for motorcycles
                        if random.random() < 0.6:  # Reduced probability
                            new_vehicle = Vehicle("motorcycle", pos)
                            vehicles[pos].append(new_vehicle)
                else:  
                    if random.random() < 0.2:  # Reduced probability
                        if not vehicles[pos] or vehicles[pos][-1].y > 50:
                            new_vehicle = Vehicle("car", pos)
                            vehicles[pos].append(new_vehicle)

    screen.fill(BLUE)

    for y in range(0, height, 20):  
        pygame.draw.line(screen, WHITE, (90, y), (90, y + 10), 2)  
        pygame.draw.line(screen, WHITE, (205, y), (205, y + 10), 2)  
    
    pygame.draw.line(screen, WHITE, (300, 0), (300, height), 5)
    pygame.draw.line(screen, WHITE, (310, 0), (310, height), 5)

    # Update and draw vehicles, calculate speeds
    for lane, lane_vehicles in vehicles.items():
        active_vehicles = []
        speeds_sum = 0
        vehicle_count = 0
        
        for vehicle in lane_vehicles:
            if vehicle.y <= height:
                vehicle.fall(lane_vehicles, safe_threshold)
                speeds_sum += vehicle.get_current_speed()
                vehicle_count += 1
                active_vehicles.append(vehicle)
        
        vehicles[lane] = active_vehicles
        
        # to update speed display every SPEED_UPDATE_INTERVAL milliseconds
        if vehicle_count > 0:
            if lane in car_positions:
                if current_time - car_velocity_data[lane]["update_time"] >= SPEED_UPDATE_INTERVAL:
                    car_velocity_data[lane]["display_speed"] = speeds_sum / vehicle_count
                    car_velocity_data[lane]["update_time"] = current_time
            elif lane in motorcycle_positions:
                if current_time - motorcycle_velocity_data[lane]["update_time"] >= SPEED_UPDATE_INTERVAL:
                    motorcycle_velocity_data[lane]["display_speed"] = speeds_sum / vehicle_count
                    motorcycle_velocity_data[lane]["update_time"] = current_time
    
    # Check for collisions after all vehicles have moved
    check_collisions()
    
    # Draw all vehicles after collision checks
    for lane, lane_vehicles in vehicles.items():
        for vehicle in lane_vehicles:
            vehicle.draw(screen)

    # Calculate elapsed time
    elapsed_time = pygame.time.get_ticks() - start_time  # in milliseconds
    elapsed_seconds = elapsed_time // 1000  #  seconds
    elapsed_minutes = elapsed_seconds // 60  #  minutes
    elapsed_seconds %= 60  # Remaining seconds

    font = pygame.font.Font(None, 24)
    y_offset = 150
    text = font.render(f"Total Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (450, y_offset))
    timer_text = font.render(f"Time: {elapsed_minutes:02}:{elapsed_seconds:02}",True, WHITE)
    screen.blit(timer_text, (400, y_offset+180))

    scaling_factor = 6.9 

    y_offset += 30
    for lane in car_positions:
        # scaling process
        scaled_speed = car_velocity_data[lane]['display_speed'] * scaling_factor
        text = font.render(f"Car Avg Speed (Lane {lane}): {scaled_speed:.2f} km/hr", True, WHITE)
        screen.blit(text, (400, y_offset))
        y_offset += 30

    for lane in motorcycle_positions:
        scaled_speed = motorcycle_velocity_data[lane]['display_speed'] * scaling_factor
        text = font.render(f"Motorcycle Avg Speed (Lane {lane}): {scaled_speed:.2f} km/hr", True, WHITE)
        screen.blit(text, (400, y_offset))
        y_offset += 30
    
    # Display collision count
    text = font.render(f"Collision Count: {collision_count}", True, RED)
    screen.blit(text, (400, y_offset))
    
    current_time = time.time()
    if current_time - last_print_time >= 1.0:  #every second printing
        car_avg, bike_avg = calculate_average_speeds()
        minutes = elapsed_minutes
        seconds = elapsed_seconds
        print(f"Time {minutes:02d}:{seconds:02d} - Car Avg Speed: {car_avg:.2f} km/hr, Bike Avg Speed: {bike_avg:.2f} km/hr")
        last_print_time = current_time

    pygame.display.flip()

pygame.quit()