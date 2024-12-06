
import pygame
import random


pygame.init()



width, height = 400, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shared lanes vehicle simulation')



WHITE = (255, 255, 255)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)


class Vehicle:
    def __init__(self, vehicle_type, lane_position):
        self.vehicle_type = vehicle_type
        self.x = lane_position  
        self.y = random.randint(-height, 0)  
        self.speed = random.uniform(1, 2) if vehicle_type == "motorcycle" else random.uniform(0.5, 1.5)
        self.original_speed = self.speed  
        self.max_speed = self.speed * 1.5 


      
        if vehicle_type == "motorcycle":
            self.size = random.randint(8, 10) 
            self.width = self.size * 2 
        elif vehicle_type == "car":
            self.width = random.randint(13, 20)  
            self.length = random.randint(23, 33) 


        self.target_x = self.x  
        self.transitioning = False  # Flag to ensure only one lane change at a time
        self.last_lane_change_time = 0  # Track the time since the last lane change


    def fall(self, vehicles_in_lane, left_lane_vehicles, right_lane_vehicles, safe_threshold):
        current_time = pygame.time.get_ticks()  

       
        self.speed = min(self.speed + 0.02, self.max_speed)

        # Adjust speed or stop based on distance to the preceding vehicle
        for other_vehicle in vehicles_in_lane:
            if other_vehicle != self and other_vehicle.y > self.y:  
                distance = other_vehicle.y - self.y
                if distance < safe_threshold:  
                    self.speed = 0  # Stop moving temporarily
                    break

        # Lane changing logic for motorcycles
        if self.vehicle_type == "motorcycle" and not self.transitioning:
           
            if (
                len(vehicles_in_lane) > 0
                and (vehicles_in_lane[0].y - self.y) < safe_threshold
                and (current_time - self.last_lane_change_time > 3000)  # 3-second cooldown
            ):
                # Evaluate left lane
                if left_lane_vehicles is not None:
                    can_switch_left = True
                    for other_vehicle in left_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < 100:  # Space check for adjacent lane
                            can_switch_left = False
                            break
                    if can_switch_left:
                        self.target_x = self.x - 200  # Move to the left lane
                        self.transitioning = True

                # Evaluate right lane
                elif right_lane_vehicles is not None:
                    can_switch_right = True
                    for other_vehicle in right_lane_vehicles:
                        if abs(other_vehicle.y - self.y) < 100:  # Space check for adjacent lane
                            can_switch_right = False
                            break
                    if can_switch_right:
                        self.target_x = self.x + 200  # Move to the right lane
                        self.transitioning = True

                # Set the cooldown for lane changes
                if self.transitioning:
                    self.last_lane_change_time = current_time

        # Smoothly transition lanes
        if self.x != self.target_x:
            if abs(self.x - self.target_x) < 1:
                self.x = self.target_x  
                self.transitioning = False
            elif self.x < self.target_x:
                self.x += 1 
            elif self.x > self.target_x:
                self.x -= 1 

        
        self.y += self.speed

        # Reset if it goes off-screen
        if self.y > height:
            self.y = random.randint(-height, 0)
            self.transitioning = False  # Reset transition state


    def draw(self, surface):
        if self.vehicle_type == "motorcycle":
            
            oval_width = self.size * 2  
            oval_height = self.size     
            pygame.draw.ellipse(surface, YELLOW, (self.x - oval_height // 2, int(self.y) - oval_width // 2, oval_height, oval_width))
        elif self.vehicle_type == "car":
            pygame.draw.rect(surface, WHITE, (self.x, int(self.y), self.width, self.length))



left_lane_positions = [60, 120]
right_lane_positions = [260, 330]
lane_positions = left_lane_positions + right_lane_positions


vehicle_types = ["motorcycle", "car"]
probabilities = [0.7, 0.3] 



vehicles = {pos: [] for pos in lane_positions}  



safe_threshold = 50


# Timers for each lane position
timers = {pos: pygame.USEREVENT + i + 1 for i, pos in enumerate(lane_positions)}



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



    pygame.draw.line(screen, WHITE, (200, 0), (200, height), 5)


    for lane in lane_positions:
        # Check if there’s a valid adjacent lane for lane-switching
        right_lane_vehicles = vehicles.get(lane + 200) if lane in left_lane_positions else None
        left_lane_vehicles = vehicles.get(lane - 200) if lane in right_lane_positions else None


        # Iterate over vehicles, updating their behavior
        for vehicle in vehicles[lane][:]:  # Use a copy of the list to avoid modification issues
            vehicle.fall(vehicles[lane], left_lane_vehicles, right_lane_vehicles, safe_threshold) 
            vehicle.draw(screen)


    pygame.display.flip()
    pygame.time.delay(30)


pygame.quit()