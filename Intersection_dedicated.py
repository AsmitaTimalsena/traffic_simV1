
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
motorcycle_safe_threshold = 50  # Safe distance for motorcycles
car_safe_threshold = 180  # Increased safe distance for cars


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


        # Vehicle size
        if vehicle_type == "motorcycle":
            self.width = random.randint(8, 12)  # Narrower width for a sleek look
            self.height = random.randint(22, 28)  # Taller height for elongation
        elif vehicle_type == "car":
            self.width = random.randint(20, 30)  # Width for cars
            self.height = random.randint(40, 50)  # Length for cars


# Inside the Vehicle class, modify the `move` method
    def move(self, vehicles_in_lane, safe_threshold):
        global total_vehicles_passed

        # Coordinates of the turning points
        car_turning_x, car_turning_y = 845, 470
        bike_turning_x, bike_turning_y = 800, 530

        # Special logic for cars at x=850 (approaching the turning point)
        if self.vehicle_type == "car" and not self.is_turning:
            # Check distance to the turning point
            distance_to_turn = abs(self.y - car_turning_y)

            # Identify the leading vehicle (most forward vehicle in the lane)
            leading_vehicle = None
            for other_vehicle in vehicles_in_lane:
                if other_vehicle != self and other_vehicle.y > self.y:
                    if not leading_vehicle or other_vehicle.y < leading_vehicle.y:
                        leading_vehicle = other_vehicle

            # Slow down trailing vehicles if the leading vehicle is near the turning point
            if distance_to_turn < 50:  # If this vehicle is close to the turning point
                for other_vehicle in vehicles_in_lane:
                    if other_vehicle != self and other_vehicle.y < self.y:  # Trailing vehicle
                        distance_behind = self.y - other_vehicle.y
                        if distance_behind < safe_threshold:  # Too close
                            other_vehicle.speed = max(self.speed - 1, 0.5)  # Reduce trailing vehicle speed

            # Start turning once at the turning point
            if self.x == 850 and self.y >= car_turning_y:
                self.is_turning = True
                self.y = car_turning_y  # Snap to the turning point
                self.x = car_turning_x  # Adjust position slightly for realism
                self.angle = 90  # Rotate the vehicle to face east

        # Add similar logic for motorcycles at x=795
        if self.vehicle_type == "motorcycle" and not self.is_turning:
            # Check distance to the turning point
            distance_to_turn = abs(self.y - bike_turning_y)

            # Identify the leading vehicle (most forward vehicle in the lane)
            leading_vehicle = None
            for other_vehicle in vehicles_in_lane:
                if other_vehicle != self and other_vehicle.y > self.y:
                    if not leading_vehicle or other_vehicle.y < leading_vehicle.y:
                        leading_vehicle = other_vehicle

            # Slow down trailing vehicles if the leading vehicle is near the turning point
            if distance_to_turn < 50:  # If this vehicle is close to the turning point
                for other_vehicle in vehicles_in_lane:
                    if other_vehicle != self and other_vehicle.y < self.y:  # Trailing vehicle
                        distance_behind = self.y - other_vehicle.y
                        if distance_behind < safe_threshold:  # Too close
                            other_vehicle.speed = max(self.speed - 1, 0.5)  # Reduce trailing vehicle speed

            # Start turning once at the turning point
            if self.x == 795 and self.y >= bike_turning_y:
                self.is_turning = True
                self.y = bike_turning_y  # Snap to the turning point
                self.x = bike_turning_x  # Adjust position slightly for realism
                self.angle = 90  # Rotate the vehicle to face east

        if self.is_turning:
            # Maintain speed during the turn
            self.speed = self.original_speed

            # Check for vehicles ahead while turning
            for other_vehicle in vehicles_in_lane:
                if other_vehicle != self and other_vehicle.x > self.x and abs(other_vehicle.y - self.y) < safe_threshold:
                    self.speed = max(other_vehicle.speed - 0.5, 0)  # Adjust speed to avoid collision
                    break
            else:
                # No vehicle ahead; allow speeding up to max_speed
                self.speed = min(self.speed + 0.5, self.max_speed)

            # Move the vehicle along the eastward path
            buffer_distance = 50  # Allow vehicles to move 50 pixels beyond screen width
            if self.vehicle_type == "car":
                if self.x < screen_width + buffer_distance:  # Continue moving right until off-screen
                    self.x += self.speed
                else:
                    # Once off-screen horizontally (with buffer), reset the car
                    self.is_turning = False
                    self.y = random.randint(-screen_height, -50)
                    self.x = 850  # Reset to initial lane position
                    self.angle = 0  # Reset angle to face south
                    total_vehicles_passed += 1

            elif self.vehicle_type == "motorcycle":
                # Move motorcycle to (800, 530) after turning
                if self.y < 530:
                    self.y += self.speed  # Move south after turning east
                elif self.x < screen_width + buffer_distance:  # Continue moving right until off-screen
                    self.x += self.speed
                else:
                    # Once off-screen horizontally (with buffer), reset the motorcycle
                    self.is_turning = False
                    self.y = random.randint(-screen_height, -50)
                    self.x = 795  # Reset to initial lane position
                    self.angle = 0  # Reset angle to face south
                    total_vehicles_passed += 1

            return  # Skip further movement logic for turning vehicles

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
            self.y = random.randint(-screen_height, -50)
            total_vehicles_passed += 1



    def draw(self, surface):
        # Create a surface for rotation
        vehicle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.vehicle_type == "motorcycle":
            pygame.draw.ellipse(
                vehicle_surface,
                YELLOW,
                (0, 0, self.width, self.height),
            )
        elif self.vehicle_type == "car":
            pygame.draw.rect(
                vehicle_surface,
                WHITE,
                (0, 0, self.width, self.height),
            )
        # Rotate the vehicle and blit it onto the main surface
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
                    if not vehicles[pos] or vehicles[pos][-1].y > safe_threshold:
                        new_vehicle = Vehicle(vehicle_type, pos)
                        vehicles[pos].append(new_vehicle)
                elif pos in car_positions and vehicle_type == "car":
                    if not vehicles[pos] or vehicles[pos][-1].y > safe_threshold:
                        new_vehicle = Vehicle(vehicle_type, pos)
                        vehicles[pos].append(new_vehicle)


    # Draw the background
    screen.blit(background_image, (0, 0))


    # Update and draw vehicles
    for lane, lane_vehicles in vehicles.items():
        for vehicle in lane_vehicles:
            vehicle.move(lane_vehicles, safe_threshold)
            vehicle.draw(screen)


    # Display the total number of vehicles passed
    font = pygame.font.Font(None, 24)
    text = font.render(f"Vehicles Passed: {total_vehicles_passed}", True, WHITE)
    screen.blit(text, (10, 10))


    pygame.display.flip()
    pygame.time.delay(20)  # Reduced delay for smoother and faster simulation


pygame.quit()
sys.exit()


