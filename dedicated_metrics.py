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

# Real-world and simulation constants
REAL_WORLD_HEIGHT = 200  # Real-world height in meters
SCREEN_HEIGHT = 700  # Screen height in pixels
FPS = 30  # Frames per second
distance_per_pixel = REAL_WORLD_HEIGHT / SCREEN_HEIGHT  # 0.286 m/pixel

car_velocity_data = {45: {"total_speed": 0, "vehicle_count": 0}, 240: {"total_speed": 0, "vehicle_count": 0}}
motorcycle_velocity_data = {120: {"total_speed": 0, "vehicle_count": 0}, 180: {"total_speed": 0, "vehicle_count": 0}}

class Vehicle:
    def __init__(self, vehicle_type, lane_position):
        """
        Initializes a vehicle with its type and lane position.
        """
        self.vehicle_type = vehicle_type
        self.x = lane_position
        self.y = random.randint(-height, 0)
        self.max_speed = random.uniform(30, 35) if vehicle_type == "motorcycle" else random.uniform(25, 30)  # Max speed in kh/hr
        self.speed = random.uniform(0.5 * self.max_speed, self.max_speed)  # Initial random speed
        self.original_speed = self.speed  # Track the original speed

        # Define vehicle size
        if vehicle_type == "motorcycle":
            self.size = random.randint(8, 10)  # Size of motorcycles
        elif vehicle_type == "car":
            self.width = random.randint(13, 20)  # Width of cars
            self.length = random.randint(23, 33)  # Length of cars

    def fall(self, vehicles_in_lane, safe_threshold):
        """
        Adjusts the vehicle's speed and position based on the proximity of other vehicles in the same lane.
        """
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
                # Too close, slow down to avoid collision
                self.speed = max(closest_vehicle.speed - 1, 0)
            elif closest_distance > 70:
                # Increase speed if safe distance exists
                self.speed = min(self.max_speed, self.original_speed + 0.5)
            else:
                # Maintain original speed
                self.speed = self.original_speed
        else:
            # No vehicle ahead, move at maximum speed
            self.speed = self.max_speed

        # Convert speed to pixels/frame for simulation
        speed_in_pixels = self.speed / distance_per_pixel / FPS
        self.y += speed_in_pixels

        # Update velocity data for averages
        if self.vehicle_type == "car" and self.x in car_velocity_data:
            lane = self.x
            car_velocity_data[lane]["total_speed"] += self.speed
            car_velocity_data[lane]["vehicle_count"] += 1
        elif self.vehicle_type == "motorcycle" and self.x in motorcycle_velocity_data:
            lane = self.x
            motorcycle_velocity_data[lane]["total_speed"] += self.speed
            motorcycle_velocity_data[lane]["vehicle_count"] += 1

        # Reset position if vehicle goes off-screen
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-SCREEN_HEIGHT, 0)
            total_vehicles_passed += 1

    def draw(self, surface):
        """
        Draws the vehicle on the given surface.
        """
        if self.vehicle_type == "motorcycle":
            oval_width = self.size * 2
            oval_height = self.size
            pygame.draw.ellipse(
                surface,
                YELLOW,
                (self.x - oval_height // 2, int(self.y) - oval_width // 2, oval_height, oval_width),
            )
        elif self.vehicle_type == "car":
            pygame.draw.rect(
                surface,
                WHITE,
                (self.x, int(self.y), self.width, self.length),
            )



# Lane positions
motorcycle_positions = [120, 180]
car_positions = [45, 240]
vehicles = {pos: [] for pos in motorcycle_positions + car_positions}

safe_threshold = 70

# Timers for lane-based vehicle generation
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(motorcycle_positions + car_positions)}
for timer in timers.values():
    pygame.time.set_timer(timer, 1000)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for pos, timer in timers.items():
            if event.type == timer:
                vehicle_type = "motorcycle" if pos in motorcycle_positions else "car"
                # Check that vehicles are spawned at reasonable intervals
                if len(vehicles[pos]) == 0:
                    vehicles[pos].append(Vehicle(vehicle_type, pos))
                elif len(vehicles[pos]) > 0:
                    last_vehicle = vehicles[pos][-1]
                    # Ensure that vehicles spawn with some minimum distance apart
                    if last_vehicle.y > 80:  # Allow spawning when the last vehicle is far enough
                        vehicles[pos].append(Vehicle(vehicle_type, pos))

    screen.fill(BLUE)

    # Draw lane markers
    for y in range(0, height, 20):
        pygame.draw.line(screen, WHITE, (90, y), (90, y + 10), 2)
        pygame.draw.line(screen, WHITE, (205, y), (205, y + 10), 2)
    pygame.draw.line(screen, WHITE, (300, 0), (300, height), 5)
    pygame.draw.line(screen, WHITE, (310, 0), (310, height), 5)

    # Update and draw vehicles
    for lane, lane_vehicles in vehicles.items():
        for vehicle in lane_vehicles:
            vehicle.fall(lane_vehicles, safe_threshold)
            vehicle.draw(screen)

    # Display metrics
    font = pygame.font.Font(None, 24)
    y_offset = 50
    text = font.render(f"Total Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (450, y_offset))

    y_offset += 30
    for lane in car_velocity_data:
        avg_speed = car_velocity_data[lane]["total_speed"] / car_velocity_data[lane]["vehicle_count"] if car_velocity_data[lane]["vehicle_count"] else 0
        text = font.render(f"Car Avg Speed (Lane {lane}): {avg_speed:.2f} km/hr", True, WHITE)
        screen.blit(text, (400, y_offset))
        y_offset += 30

    for lane in motorcycle_velocity_data:
        avg_speed = motorcycle_velocity_data[lane]["total_speed"] / motorcycle_velocity_data[lane]["vehicle_count"] if motorcycle_velocity_data[lane]["vehicle_count"] else 0
        text = font.render(f"Motorcycle Avg Speed (Lane {lane}): {avg_speed:.2f} km/hr", True, WHITE)
        screen.blit(text, (400, y_offset))
        y_offset += 30

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
