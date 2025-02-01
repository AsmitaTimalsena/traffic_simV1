import pygame
import random
import sys

pygame.init()


# Screen dimensions
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("North Road Vehicle Simulation")


# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)


# Load and scale the background image
background_image = pygame.image.load("dedicated_laneIMG1.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


# Global variables
total_vehicles_passed = 0
motorcycle_positions = [760, 795]  # Middle lanes for motorcycles
car_positions = [680, 850]        # Outer lanes for cars
motorcycle_safe_threshold = 50  # Safe distance for motorcycles
car_safe_threshold = 180  # Increased safe distance for cars
max_vehicles_per_lane = 10  # Limit the number of vehicles in each lane

dash_coordinates = [
    # Traffic lights
    # north road
    (760, 420), (680, 420),
    # East road
    (880, 590),
    # South road
    (600, 690),
    # West road
    (400, 520),
]




dash_length = 20  # Length of the dash
dash_thickness = 5  # Thickness of the dash




# Initial color for traffic lights
dash_colors = {coord: (255, 0, 0) for coord in dash_coordinates}  # Red initially
current_green_index = 0




directions = [
    [(760, 420), (680, 420)],  # North
    [(600, 690)],  # South
    [(880, 590)],  # East
    [(400, 520)],  # West
]




for coord in directions[current_green_index]:
    dash_colors[coord] = (0, 255, 0)  # Set the first direction's lights to green




color_change_time = 30000  # Time interval in milliseconds
last_color_change = pygame.time.get_ticks()




# Vehicle class
class Vehicle:
    def __init__(self, vehicle_type, lane_position):
        self.vehicle_type = vehicle_type
        self.x = lane_position
        self.y = random.randint(-screen_height, 0)  # Start off-screen
        self.max_speed = 4 if vehicle_type == "motorcycle" else 3
        self.speed = random.uniform(2.5, 4.0) if vehicle_type == "motorcycle" else random.uniform(1.5, 3.0)
        self.original_speed = self.speed
        self.is_turning = False  # Tracks if the vehicle is turning
        self.angle = 0  # Initial angle (facing south)
        self.has_crossed_light = False  # Tracks if the vehicle has crossed the traffic light
        self.has_been_counted = False  # Initialize counting flag


        # Vehicle size
        if vehicle_type == "motorcycle":
            self.width = random.randint(8, 12)  # Narrower width for a sleek look
            self.height = random.randint(22, 28)  # Taller height for elongation
        elif vehicle_type == "car":
            self.width = random.randint(20, 30)  # Width for cars
            self.height = random.randint(40, 50)  # Length for cars


        # Randomly decide if vehicle will turn west or go straight for specific lanes
        self.turn_west = False
        if self.x in [680, 760]:  # Only for lanes 680 and 760
            self.turn_west = random.random() < 0.5  # 50% chance of turning west




    def move(self, vehicles_in_lane, safe_threshold):
        global total_vehicles_passed


        # Coordinates for east and west turning points
        car_turning_x, car_turning_y = 845, 470  # East turn for cars
        bike_turning_x, bike_turning_y = 800, 530  # East turn for motorcycles
        car_turning_x1, car_turning_y1 = 680, 590  # West turn for cars
        bike_turning_x1, bike_turning_y1 = 760, 640  # West turn for motorcycles


        # Traffic light logic for lanes 760 and 680
        if self.x in (760, 680):  # Only apply to lanes 760 (motorcycles) and 680 (cars)
            light_color = dash_colors.get((self.x, 420), (255, 0, 0))  # Default to red if no light is found
            light_stop_y = 410 # 20 units before the traffic dash line


            distance_to_light = light_stop_y - (self.y + self.height)


            # Check if the vehicle has already crossed the light
            if not self.has_crossed_light:
                if light_color == (0, 255, 0):  # Green light
                    if distance_to_light <= 0:
                        self.has_crossed_light = True  # Mark as having crossed the light
                elif light_color == (255, 0, 0):  # Red light
                    if distance_to_light <= 30 and distance_to_light > 0:  # If within stopping range
                        self.speed = max(0, self.speed - 0.5)  # Gradually stop
                        if distance_to_light <= 5:  # Close enough to the stop line
                            self.speed = 0
                    elif distance_to_light <= 0:  # If already beyond the stopping point
                        self.speed = self.original_speed  # Allow vehicle to continue
                    else:
                    # Queue logic: Vehicles behind maintain safe distance
                        closest_vehicle = None
                        closest_distance = float('inf')

                        # Find the closest vehicle ahead
                        for other_vehicle in vehicles_in_lane:
                            if other_vehicle != self and other_vehicle.y > self.y:
                                distance = other_vehicle.y - self.y
                                if distance < closest_distance:
                                    closest_distance = distance
                                    closest_vehicle = other_vehicle

                        # Adjust speed for vehicles behind
                        if closest_vehicle:
                            if closest_distance < 80:  # Maintain 80 units of distance
                                self.speed = max(0, closest_vehicle.speed - 0.5)  # Gradually stop
                            else:
                                self.speed = self.original_speed  # Resume normal speed
                        else:
                            self.speed = self.original_speed  # No vehicle ahead, move normally

                    self.y += self.speed  # Update position based on speed
                    return  # Skip further logic for these lanes when stopping for the light

        # Handle turning logic
        if not self.is_turning:
            if self.vehicle_type == "car":
                if self.x == 850 and self.y >= car_turning_y:  # Turning east
                    self.is_turning = True
                    self.y = car_turning_y
                    self.angle = 90  # Face east
                elif self.x == 680 and self.y >= car_turning_y1 and self.turn_west:  # Turning west
                    self.is_turning = True
                    self.y = car_turning_y1
                    self.angle = 270  # Face west
            elif self.vehicle_type == "motorcycle":
                if self.x == 795 and self.y >= bike_turning_y:  # Turning east
                    self.is_turning = True
                    self.y = bike_turning_y
                    self.angle = 90  # Face east
                elif self.x == 760 and self.y >= bike_turning_y1 and self.turn_west:  # Turning west
                    self.is_turning = True
                    self.y = bike_turning_y1
                    self.angle = 270  # Face west


        if self.is_turning:
            # Handle eastward and westward turning movement
            if self.angle == 90:  # Eastward movement
                self.x += self.speed
            elif self.angle == 270:  # Westward movement
                self.x -= self.speed


            # After turning, reset speed to original speed and avoid unnecessary slowdowns
            if self.x > screen_width + 50 or self.x < -50:  # Buffer distance
                self.is_turning = False
                self.y = random.randint(-screen_height, -50)
                if self.vehicle_type == "car":
                    self.x = 850 if self.angle == 90 else 680  # Reset car to correct lane
                elif self.vehicle_type == "motorcycle":
                    self.x = 795 if self.angle == 90 else 760  # Reset motorcycle to correct lane
                self.angle = 0  # Reset angle
                self.speed = self.original_speed  # Reset speed after turn
                total_vehicles_passed += 1
            return  # Skip further movement logic during turning


        # Normal movement logic for vehicles moving straight
        closest_vehicle = None
        closest_distance = float('inf')


        # Find the closest vehicle ahead
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:
                distance = other_vehicle.y - self.y
                if distance < closest_distance:
                    closest_distance = distance
                    closest_vehicle = other_vehicle


        # Adjust speed based on distance to the closest vehicle
        if closest_vehicle:
            if closest_distance < safe_threshold:
                self.speed = max(closest_vehicle.speed - 0.5, 0)  # Slow down to avoid collision
            elif closest_distance > 70:
                self.speed = min(self.max_speed, self.original_speed + 0.5)  # Speed up
            else:
                self.speed = self.original_speed  # Maintain original speed
        else:
            self.speed = self.max_speed  # No vehicle ahead, move at max speed


        self.y += self.speed


        # If off-screen, reset position and count as passed
        if self.y > screen_height:
            if not self.has_been_counted:
                total_vehicles_passed += 1
                self.has_been_counted = True
            self.reset_vehicle()

    def reset_vehicle(self):
        self.y = random.randint(-screen_height, -50)
        self.speed = self.original_speed
        self.is_turning = False
        self.has_crossed_light = False
        self.has_been_counted = False  # Reset counting flag

    def draw(self, surface):
        vehicle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.vehicle_type == "motorcycle":
            pygame.draw.ellipse(vehicle_surface, YELLOW, (0, 0, self.width, self.height))
        elif self.vehicle_type == "car":
            pygame.draw.rect(vehicle_surface, WHITE, (0, 0, self.width, self.height))
        rotated_surface = pygame.transform.rotate(vehicle_surface, -self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        surface.blit(rotated_surface, rotated_rect)

# Create vehicles for each lane
vehicles = {pos: [] for pos in motorcycle_positions + car_positions}

# Timers for each lane position
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(motorcycle_positions + car_positions)}
for timer in timers.values():
    pygame.time.set_timer(timer, 1000)  # Generate a new vehicle every second

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




        # Generate vehicles for each lane position
        for pos, timer in timers.items():
            if event.type == timer:
                # Generate vehicle type based on probability
                vehicle_type = random.choices(
                    ["motorcycle", "car"], [0.65, 0.35], k=1
                )[0]




                # Set the safe threshold based on vehicle type
                if vehicle_type == "motorcycle":
                    safe_threshold = motorcycle_safe_threshold  # Safe distance for motorcycles
                else:
                    safe_threshold = car_safe_threshold  # Safe distance for cars




                # Generate motorcycles in the middle lanes and cars in the outer lanes
                if pos in motorcycle_positions and vehicle_type == "motorcycle":
                    if len(vehicles[pos]) < max_vehicles_per_lane and (not vehicles[pos] or vehicles[pos][-1].y > safe_threshold):
                        new_vehicle = Vehicle(vehicle_type, pos)
                        vehicles[pos].append(new_vehicle)
                elif pos in car_positions and vehicle_type == "car":
                    if len(vehicles[pos]) < max_vehicles_per_lane and (not vehicles[pos] or vehicles[pos][-1].y > safe_threshold):
                        new_vehicle = Vehicle(vehicle_type, pos)
                        vehicles[pos].append(new_vehicle)




    # Get the current time
    current_time = pygame.time.get_ticks()




     # Change traffic light colors every 5 seconds
    if current_time - last_color_change >= color_change_time:
        # Reset all lights to red
        for coord in dash_colors:
            dash_colors[coord] = (255, 0, 0)
        # Set the current direction to green
        current_green_index = (current_green_index + 1) % len(directions)
        for coord in directions[current_green_index]:
            dash_colors[coord] = (0, 255, 0)
        # Update the last color change time
        last_color_change = current_time




    # Draw the background and traffic lights
    screen.blit(background_image, (0, 0))




    for (x, y) in dash_coordinates:
        if x == 880 or x == 400:  # East and West roads (vertical dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x, y - dash_length // 2), (x, y + dash_length // 2), dash_thickness)
        else:  # North and South roads (horizontal dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x - dash_length // 2, y), (x + dash_length // 2, y), dash_thickness)




    # Update and draw vehicles
    for lane, lane_vehicles in vehicles.items():
        for vehicle in lane_vehicles:
            vehicle.move(lane_vehicles, car_safe_threshold if lane in car_positions else motorcycle_safe_threshold)
            vehicle.draw(screen)




    # Display the total number of vehicles passed
    font = pygame.font.Font(None, 24)
    text = font.render(f"Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (10, 10))




    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Adjust frame rate for smoother simulation




pygame.quit()
sys.exit()
