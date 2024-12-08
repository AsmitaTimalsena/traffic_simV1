import pygame
import random

pygame.init()

width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shared lanes vehicle simulation')

WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)

total_vehicles_passed = 0

# Updated velocity data for the new lanes
car_velocity_data = {45: {"total_speed": 0, "vehicle_count": 0}, 240: {"total_speed": 0, "vehicle_count": 0}}
motorcycle_velocity_data = {120: {"total_speed": 0, "vehicle_count": 0}, 180: {"total_speed": 0, "vehicle_count": 0}}

class Vehicle:
    def __init__(self, vehicle_type, lane_position):
        self.vehicle_type = vehicle_type
        self.x = lane_position
        self.y = random.randint(-height, 0) 
        self.max_speed = 3 if vehicle_type == "motorcycle" else 2
        self.speed = random.uniform(1, 2) if vehicle_type == "motorcycle" else random.uniform(0.5, 1.5)
        self.original_speed = self.speed  

        if vehicle_type == "motorcycle":
            self.size = random.randint(8, 10) 
        elif vehicle_type == "car":
            self.width = random.randint(13, 20)
            self.length = random.randint(23, 33)

    def fall(self, vehicles_in_lane, safe_threshold):
        global total_vehicles_passed, car_velocity_data, motorcycle_velocity_data

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
                self.speed = max(closest_vehicle.speed - 0.5, 0)
            elif closest_distance > 70:
                # Safe distance, increase speed slightly
                self.speed = min(self.max_speed, self.original_speed + 0.5)
            else:
                # Moderate distance, maintain original speed
                self.speed = self.original_speed
        else:
            # No vehicle ahead, move at maximum speed
            self.speed = self.max_speed

        self.y += self.speed

        # Update the velocity data for average calculation
        if self.vehicle_type == "car":
            if self.x == 45 or self.x == 240:  # Updated lanes for cars
                lane = self.x
                car_velocity_data[lane]["total_speed"] += self.speed
                car_velocity_data[lane]["vehicle_count"] += 1
        elif self.vehicle_type == "motorcycle":
            if self.x == 120 or self.x == 180:  # Updated lanes for motorcycles
                lane = self.x
                motorcycle_velocity_data[lane]["total_speed"] += self.speed
                motorcycle_velocity_data[lane]["vehicle_count"] += 1

        # If the vehicle goes off-screen, reset its position and update the counter
        if self.y > height:
            self.y = random.randint(-height, 0)
            total_vehicles_passed += 1  

    def draw(self, surface):
        if self.vehicle_type == "motorcycle":
            oval_width = self.size * 2
            oval_height = self.size     
            pygame.draw.ellipse(surface, YELLOW, (self.x - oval_height // 2, int(self.y) - oval_width // 2, oval_height, oval_width))
        elif self.vehicle_type == "car":
            pygame.draw.rect(surface, WHITE, (self.x, int(self.y), self.width, self.length))

# Updated lane positions
motorcycle_positions = [120, 180]
car_positions = [45, 240]

vehicle_types = ["motorcycle", "car"]
probabilities = [0.7, 0.3]  # 70% for motorcycles, 30% for cars

vehicles = {pos: [] for pos in motorcycle_positions + car_positions}

safe_threshold = 50

# Timers for vehicle generation in lanes
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(motorcycle_positions + car_positions)}

for timer in timers.values():
    pygame.time.set_timer(timer, 1000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Generate vehicles for each lane position independently
        for pos, timer in timers.items():
            if event.type == timer:
                # Determine vehicle type based on lane position
                if pos in motorcycle_positions:
                    vehicle_type = "motorcycle"
                elif pos in car_positions:
                    vehicle_type = "car"
                else:
                    continue

                # Add vehicles with minimal distance between them
                if not vehicles[pos] or vehicles[pos][-1].y > 50:
                    new_vehicle = Vehicle(vehicle_type, pos)
                    vehicles[pos].append(new_vehicle)

    screen.fill(BLUE)
   
    # Draw lane markers
    for y in range(0, height, 20):  # Adjust the step to control the gap size
        pygame.draw.line(screen, WHITE, (90, y), (90, y + 10), 2)  
        pygame.draw.line(screen, WHITE, (205, y), (205, y + 10), 2)  
   
    pygame.draw.line(screen, WHITE, (300, 0), (300, height), 5)
    pygame.draw.line(screen, WHITE, (310, 0), (310, height), 5)

    # Update and draw vehicles (only in the first 400px wide area)
    for lane, lane_vehicles in vehicles.items():
        for vehicle in lane_vehicles:
            vehicle.fall(lane_vehicles, safe_threshold)  
            if vehicle.x < 400:  
                vehicle.draw(screen)

    # Display vehicles passed (on the right side of the screen)
    font = pygame.font.Font(None, 24)
    text = font.render(f"Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (450, 50))  

    # Display average velocity for cars (in lanes 45 and 240)
    y_offset = 80  
    for lane in car_velocity_data:
        if car_velocity_data[lane]["vehicle_count"] > 0:
            avg_speed = car_velocity_data[lane]["total_speed"] / car_velocity_data[lane]["vehicle_count"]
            text = font.render(f"Car Avg Speed (Lane {lane}): {avg_speed:.2f}", True, WHITE)
            screen.blit(text, (450, y_offset))
            y_offset += 30  

    # Display average velocity for motorcycles (in lanes 120 and 180)
    for lane in motorcycle_velocity_data:
        if motorcycle_velocity_data[lane]["vehicle_count"] > 0:
            avg_speed = motorcycle_velocity_data[lane]["total_speed"] / motorcycle_velocity_data[lane]["vehicle_count"]
            text = font.render(f"Motorcycle Avg Speed (Lane {lane}): {avg_speed:.2f}", True, WHITE)
            screen.blit(text, (450, y_offset))
            y_offset += 30 

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
