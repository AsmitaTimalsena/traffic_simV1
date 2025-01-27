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
background_image = pygame.image.load("dedicated_laneIMG.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


# Global variables
total_vehicles_passed = 0
motorcycle_positions = [760, 795]  # Middle lanes for motorcycles
car_positions = [680, 850]        # Outer lanes for cars
motorcycle_safe_threshold = 50    # Safe distance for motorcycles
car_safe_threshold = 180          # Safe distance for cars


 # Traffic lights
dash_coordinates = [
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
color_change_time = 5000  # Time interval in milliseconds
last_color_change = pygame.time.get_ticks()
current_green_index = 0

directions = [
    [(760, 420), (680, 420)],  # North
    [(600, 690)],  # South
    [(880, 590)],  # East
    [(400, 520)],  # West
]



class Vehicle:
    def __init__(self, vehicle_type, lane_position):
        self.vehicle_type = vehicle_type
        self.x = lane_position
        self.y = random.randint(-screen_height, 0)
        self.max_speed = 4 if vehicle_type == "motorcycle" else 3
        self.speed = random.uniform(2.5, 4.0) if vehicle_type == "motorcycle" else random.uniform(1.5, 3.0)
        self.original_speed = self.speed
        self.is_turning = False
        self.angle = 0
        self.turn_direction = None
        self.distance_travelled = 0


        # Vehicles in 795 and 850 always turn east
        self.should_turn = True if self.x in [795, 850] else random.choice([True, False])


        # Vehicle size
        if vehicle_type == "motorcycle":
            self.width = random.randint(8, 12)
            self.height = random.randint(22, 28)
        else:
            self.width = random.randint(20, 30)
            self.height = random.randint(40, 50)


    def move(self, vehicles_in_lane, safe_threshold):
        global total_vehicles_passed

        # Define turn points for vehicles (EAST_TURNS, WEST_TURNS logic)
        EAST_TURNS = {
            "car": {"start_x": 850, "turn_x": 845, "turn_y": 470},
            "motorcycle": {"start_x": 795, "turn_x": 800, "turn_y": 530}
        }

        WEST_TURNS = {
            "car": {"start_x": 680, "turn_x": 680, "turn_y": 590},
            "motorcycle": {"start_x": 760, "turn_x": 760, "turn_y": 640}
        }

        # Collision prevention logic
        closest_vehicle = None
        closest_distance = float('inf')

        # Find the closest vehicle ahead in the same lane
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:
                # Check both vertical and horizontal proximity
                vertical_distance = other_vehicle.y - self.y
                horizontal_distance = abs(other_vehicle.x - self.x)
                
                # More stringent collision check
                if vertical_distance < closest_distance and horizontal_distance < (self.width + other_vehicle.width) / 2:
                    closest_distance = vertical_distance
                    closest_vehicle = other_vehicle

        # Adjust speed based on the closest vehicle
        if closest_vehicle:
            # Increase safe following distance
            if closest_distance < safe_threshold * 1.5:
                # Slow down more gradually
                self.speed = max(closest_vehicle.speed - 0.3, 0)
            elif closest_distance > 70:
                self.speed = min(self.max_speed, self.original_speed + 0.5)
            else:
                self.speed = self.original_speed
        else:
            self.speed = self.max_speed

        # Ensure vehicles maintain a safe distance from each other
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:
                distance_to_next_vehicle = other_vehicle.y - self.y
                if distance_to_next_vehicle < safe_threshold:  # If too close
                    self.speed = max(self.speed - 0.5, 0)  # Slow down
                break  # Only check the closest vehicle ahead

        # Check if the vehicle needs to turn (EAST/WEST turns logic)
        if not self.is_turning:
            if (self.vehicle_type == "car" and self.x == EAST_TURNS["car"]["start_x"] and self.y >= EAST_TURNS["car"]["turn_y"]):
                if self.should_turn:
                    self.is_turning = True
                    self.x = EAST_TURNS["car"]["turn_x"]
                    self.y = EAST_TURNS["car"]["turn_y"]
                    self.angle = 90
                    self.turn_direction = "east"

            elif (self.vehicle_type == "motorcycle" and self.x == EAST_TURNS["motorcycle"]["start_x"] and self.y >= EAST_TURNS["motorcycle"]["turn_y"]):
                if self.should_turn:
                    self.is_turning = True
                    self.x = EAST_TURNS["motorcycle"]["turn_x"]
                    self.y = EAST_TURNS["motorcycle"]["turn_y"]
                    self.angle = 90
                    self.turn_direction = "east"

            # Handle west turns (left turns)
            elif (self.vehicle_type == "car" and abs(self.x - WEST_TURNS["car"]["start_x"]) < 10 and self.y >= WEST_TURNS["car"]["turn_y"]):
                if self.should_turn:
                    self.is_turning = True
                    self.x = WEST_TURNS["car"]["turn_x"]
                    self.y = WEST_TURNS["car"]["turn_y"]
                    self.angle = 270
                    self.turn_direction = "west"

            elif (self.vehicle_type == "motorcycle" and abs(self.x - WEST_TURNS["motorcycle"]["start_x"]) < 10 and self.y >= WEST_TURNS["motorcycle"]["turn_y"]):
                if self.should_turn:
                    self.is_turning = True
                    self.x = WEST_TURNS["motorcycle"]["turn_x"]
                    self.y = WEST_TURNS["motorcycle"]["turn_y"]
                    self.angle = 270
                    self.turn_direction = "west"

        # Handle turning movement (for vehicles making turns)
        if self.is_turning:
            buffer_distance = 60
            if self.turn_direction == "east":
                if self.x < screen_width + buffer_distance:
                    self.x += self.speed
                else:
                    self.reset_position()
                    total_vehicles_passed += 1
            elif self.turn_direction == "west":
                if self.x > -self.width:
                    self.x -= self.speed
                else:
                    self.reset_position()
                    total_vehicles_passed += 1
            return

        # Normal straight movement (no turn)
        self.y += self.speed

        # If vehicle reaches the bottom of the screen, reset position
        if self.y > screen_height:
            self.reset_position()
            total_vehicles_passed += 1

    # Reset position of the vehicle when it reaches the screen's bottom
    def reset_position(self):
        self.is_turning = False
        self.y = random.randint(-screen_height, -50)
        if self.vehicle_type == "car":
            self.x = 850 if self.x > screen_width / 2 else 680
        else:
            self.x = 795 if self.x > screen_width / 2 else 760
        self.angle = 0
        self.turn_direction = None
        self.distance_travelled = 0


        # Vehicles in specific positions always turn east
        self.should_turn = True if self.x in [795, 850] else random.choice([True, False])


    def draw(self, surface):
        vehicle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.vehicle_type == "motorcycle":
            pygame.draw.ellipse(vehicle_surface, YELLOW, (0, 0, self.width, self.height))
        else:
            pygame.draw.rect(vehicle_surface, WHITE, (0, 0, self.width, self.height))
       
        rotated_surface = pygame.transform.rotate(vehicle_surface, -self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        surface.blit(rotated_surface, rotated_rect)


# Create vehicles for each lane
vehicles = {pos: [] for pos in motorcycle_positions + car_positions}


# Timers for each lane position
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(motorcycle_positions + car_positions)}
for timer in timers.values():
    pygame.time.set_timer(timer, 1000)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # Generate vehicles for each lane position
        for pos, timer in timers.items():
            if event.type == timer:
                vehicle_type = random.choices(["motorcycle", "car"], [0.65, 0.35], k=1)[0]
                safe_threshold = motorcycle_safe_threshold if vehicle_type == "motorcycle" else car_safe_threshold

                # Ensure a vehicle is added only if the last vehicle is at least 60 units down the screen
                if pos in motorcycle_positions and vehicle_type == "motorcycle":
                    if not vehicles[pos] or vehicles[pos][-1].y > -60:  # Check 60-unit rule
                        new_vehicle = Vehicle(vehicle_type, pos)
                        vehicles[pos].append(new_vehicle)
                elif pos in car_positions and vehicle_type == "car":
                    if not vehicles[pos] or vehicles[pos][-1].y > -60:  # Check 60-unit rule
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
        for coord in directions[current_green_index]:
            dash_colors[coord] = (0, 255, 0)
        # Move to the next direction
        current_green_index = (current_green_index + 1) % len(directions)
        last_color_change = current_time


    # Draw background
    screen.blit(background_image, (0, 0))

    for (x, y) in dash_coordinates:
        if x == 880 or x == 400:  # East and West roads (vertical dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x, y - dash_length // 2), (x, y + dash_length // 2), dash_thickness)
        else:  # North and South roads (horizontal dashes)
            pygame.draw.line(screen, dash_colors[(x, y)], (x - dash_length // 2, y), (x + dash_length // 2, y), dash_thickness)



    # Update and draw vehicles
    for lane, lane_vehicles in vehicles.items():
        for vehicle in lane_vehicles:
            vehicle.move(lane_vehicles, car_safe_threshold if vehicle.vehicle_type == "car" else motorcycle_safe_threshold)
            vehicle.draw(screen)


    # Display vehicle count
    font = pygame.font.Font(None, 24)
    text = font.render(f"Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (10, 10))


    pygame.display.flip()
    pygame.time.delay(20)


pygame.quit()
sys.exit()
